#!/usr/bin/env node
/**
 * Page checks for a repo with no build step: every local href and src must
 * resolve on disk, every inline script must parse, and every page must carry
 * the meta tags that make it usable on a phone and legible in a link preview.
 *
 * Catches the two failures that actually happen here — a moved file nobody
 * relinked, and a typo inside a <script> block that only shows up in a browser.
 */
import { readFileSync, readdirSync, statSync, existsSync } from "node:fs";
import { join, dirname, resolve, relative, extname } from "node:path";
import { fileURLToPath } from "node:url";
import vm from "node:vm";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const SKIP_DIRS = new Set([".git", "node_modules", ".github"]);

function walk(dir, out = []) {
  for (const name of readdirSync(dir)) {
    if (SKIP_DIRS.has(name)) continue;
    const full = join(dir, name);
    if (statSync(full).isDirectory()) walk(full, out);
    else if (extname(full) === ".html") out.push(full);
  }
  return out;
}

const errors = [];
const pages = walk(root);

for (const file of pages) {
  const rel = relative(root, file);
  const html = readFileSync(file, "utf8");
  const here = dirname(file);
  const fail = (m) => errors.push(`${rel}: ${m}`);

  // ——— required head furniture ———
  if (!/^<!DOCTYPE html>/i.test(html.trim())) fail("missing <!DOCTYPE html>");
  if (!/<html[^>]+lang=/i.test(html)) fail("<html> has no lang attribute");
  if (!/<meta[^>]+name=["']viewport["']/i.test(html)) fail("no viewport meta — will render at desktop width on a phone");
  if (!/<meta[^>]+charset=/i.test(html)) fail("no charset meta");
  if (!/<title>[^<]+<\/title>/i.test(html)) fail("no non-empty <title>");

  // ——— local links and assets resolve ———
  const refs = [...html.matchAll(/(?:href|src)=["']([^"']+)["']/gi)].map((m) => m[1]);
  for (const ref of refs) {
    if (/^(https?:|mailto:|data:|#|\/\/)/i.test(ref)) continue;
    const [path] = ref.split(/[?#]/);
    if (!path) continue;
    // A leading slash is site-root-relative once deployed, not filesystem-absolute.
    // path.join() would treat that slash as an absolute path and drop `root`.
    const target = path.startsWith("/") ? join(root, path.slice(1)) : resolve(here, path);
    const ok = existsSync(target) && (statSync(target).isFile() || existsSync(join(target, "index.html")));
    if (!ok) fail(`dead local reference "${ref}"`);
  }

  // ——— inline scripts parse ———
  const scripts = [...html.matchAll(/<script(?![^>]*\bsrc=)([^>]*)>([\s\S]*?)<\/script>/gi)];
  for (const [i, m] of scripts.entries()) {
    const attrs = m[1] || "";
    const body = m[2];
    if (/type=["']application\/(ld\+)?json["']/i.test(attrs)) {
      try { JSON.parse(body); } catch (e) { fail(`inline JSON block ${i + 1} is invalid: ${e.message}`); }
      continue;
    }
    try { new vm.Script(body, { filename: `${rel}#script${i + 1}` }); }
    catch (e) { fail(`inline script ${i + 1} does not parse: ${e.message}`); }
  }

  // ——— every form control is labelled ———
  const ids = new Set([...html.matchAll(/id=["']([^"']+)["']/g)].map((m) => m[1]));
  for (const m of html.matchAll(/<label[^>]+for=["']([^"']+)["']/g)) {
    if (!ids.has(m[1])) fail(`<label for="${m[1]}"> points at no element`);
  }
}

// ——— data files referenced by the tools exist and parse ———
for (const f of ["data/vendors.json", "data/vendors.schema.json", "data/intake-questions.json"]) {
  try { JSON.parse(readFileSync(join(root, f), "utf8")); }
  catch (e) { errors.push(`${f}: ${e.message}`); }
}

for (const e of errors) console.error(`  ERROR ${e}`);
console.log(`\n${pages.length} pages checked · ${errors.length} error${errors.length === 1 ? "" : "s"}`);
process.exit(errors.length ? 1 : 0);
