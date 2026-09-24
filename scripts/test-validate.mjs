#!/usr/bin/env node
/**
 * Negative tests for the register validator. A rule nobody has watched fail
 * is a rule you are trusting on faith — these make each one fail on purpose.
 */
import { execFileSync } from "node:child_process";
import { mkdtempSync, writeFileSync, readFileSync, cpSync, mkdirSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const good = JSON.parse(readFileSync(join(root, "data/vendors.json"), "utf8"));

const clone = (fn) => {
  const d = structuredClone(good);
  fn(d.vendors[0], d);
  return d;
};

const cases = [
  ["the register as committed", good, true],
  ["BAA claimed with no source or date", clone((v) => { v.baa.status = "offered"; }), false],
  ["BAA claimed with a source but no date", clone((v) => { v.baa.status = "offered"; v.baa.source_url = "https://example.com/baa"; }), false],
  ["tier-gated BAA with no tier named", clone((v) => {
      v.baa.status = "offered_on_tier"; v.baa.source_url = "https://example.com/baa"; v.baa.verified_on = "2026-01-15";
    }), false],
  ["a fully sourced BAA claim", clone((v) => {
      v.baa.status = "offered_on_tier"; v.baa.tier = "Enterprise";
      v.baa.source_url = "https://example.com/baa"; v.baa.verified_on = "2026-01-15";
    }), true],
  ["a price with no date checked", clone((v) => { v.pricing.from_usd_month = 29; }), false],
  ["a price with a date checked", clone((v) => { v.pricing.from_usd_month = 29; v.pricing.checked_on = "2026-01-15"; }), true],
  ["duplicate ids", clone((v, d) => { d.vendors[1].id = v.id; }), false],
  ["an unknown category", clone((v) => { v.category = "vibes"; }), false],
  ["a malformed url", clone((v) => { v.url = "not-a-url"; }), false],
  ["a missing required field", clone((v) => { delete v.what_it_does; }), false],
  ["a stray field", clone((v) => { v.favourite_colour = "teal"; }), false]
];

const dir = mkdtempSync(join(tmpdir(), "fc-validate-"));
mkdirSync(join(dir, "data"), { recursive: true });
cpSync(join(root, "scripts"), join(dir, "scripts"), { recursive: true });
cpSync(join(root, "data/vendors.schema.json"), join(dir, "data/vendors.schema.json"));

let failed = 0;
for (const [name, data, shouldPass] of cases) {
  writeFileSync(join(dir, "data/vendors.json"), JSON.stringify(data, null, 2));
  let passed;
  try {
    execFileSync(process.execPath, [join(dir, "scripts/validate-data.mjs")], { stdio: "pipe" });
    passed = true;
  } catch {
    passed = false;
  }
  const ok = passed === shouldPass;
  if (!ok) failed++;
  console.log(`  ${ok ? "ok  " : "FAIL"}  ${name} — ${shouldPass ? "should pass" : "should be rejected"}`);
}

console.log(`\n${cases.length - failed}/${cases.length} validator tests passed`);
process.exit(failed ? 1 : 0);
