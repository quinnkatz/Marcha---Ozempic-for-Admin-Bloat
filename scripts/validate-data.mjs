#!/usr/bin/env node
/**
 * Validates data/vendors.json against data/vendors.schema.json.
 *
 * The rule that matters is the last one: a BAA status other than "unverified"
 * needs a source URL and a date. That is the whole difference between a
 * register you can hand a practice and a guess with a table around it.
 *
 * Zero dependencies on purpose — this repo has no build step and should not
 * grow one just to check twenty rows of JSON.
 */
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const here = dirname(fileURLToPath(import.meta.url));
const root = join(here, "..");

const errors = [];
const warnings = [];
const fail = (where, msg) => errors.push(`${where}: ${msg}`);
const warn = (where, msg) => warnings.push(`${where}: ${msg}`);

const readJSON = (rel) => {
  try {
    return JSON.parse(readFileSync(join(root, rel), "utf8"));
  } catch (e) {
    console.error(`Could not read ${rel}: ${e.message}`);
    process.exit(1);
  }
};

const schema = readJSON("data/vendors.schema.json");
const data = readJSON("data/vendors.json");
const def = schema.$defs.vendor;
const props = def.properties;

const enumOf = (path) => path.split(".").reduce((o, k) => o?.[k], props)?.enum ?? [];
const CATEGORIES = enumOf("category");
const PHI = enumOf("phi_exposure");
const BAA_STATUS = props.baa.properties.status.enum;
const EFFORT = props.setup.properties.effort.enum;
const ISO_DATE = /^\d{4}-\d{2}-\d{2}$/;

if (!Number.isInteger(data.version) || data.version < 1) fail("root", "version must be a positive integer");
if (!Array.isArray(data.vendors)) {
  fail("root", "vendors must be an array");
} else {
  const seenIds = new Set();
  const seenNames = new Set();

  for (const [i, v] of data.vendors.entries()) {
    const where = `vendors[${i}]${v?.id ? ` (${v.id})` : ""}`;

    for (const key of def.required) {
      if (v?.[key] === undefined) fail(where, `missing required field "${key}"`);
    }
    if (!v || typeof v !== "object") continue;

    for (const key of Object.keys(v)) {
      if (!(key in props)) fail(where, `unknown field "${key}"`);
    }

    if (!/^[a-z0-9-]+$/.test(v.id ?? "")) fail(where, `id "${v.id}" must be lowercase letters, digits and hyphens`);
    if (seenIds.has(v.id)) fail(where, `duplicate id "${v.id}"`);
    seenIds.add(v.id);

    const nameKey = String(v.name ?? "").trim().toLowerCase();
    if (seenNames.has(nameKey)) warn(where, `"${v.name}" appears more than once`);
    seenNames.add(nameKey);

    if (!CATEGORIES.includes(v.category)) fail(where, `category "${v.category}" is not one of: ${CATEGORIES.join(", ")}`);
    if (!PHI.includes(v.phi_exposure)) fail(where, `phi_exposure "${v.phi_exposure}" is not one of: ${PHI.join(", ")}`);
    if (!String(v.what_it_does ?? "").trim()) fail(where, "what_it_does is empty");

    try {
      const u = new URL(v.url);
      if (u.protocol !== "https:") warn(where, `url is not https`);
    } catch {
      fail(where, `url "${v.url}" is not a valid URL`);
    }

    // ——— BAA: the rule this file exists for ———
    const baa = v.baa ?? {};
    if (!BAA_STATUS.includes(baa.status)) {
      fail(where, `baa.status "${baa.status}" is not one of: ${BAA_STATUS.join(", ")}`);
    } else if (baa.status !== "unverified") {
      if (!baa.source_url) fail(where, `baa.status is "${baa.status}" with no source_url — say where the vendor commits to it, in writing`);
      if (!ISO_DATE.test(baa.verified_on ?? "")) fail(where, `baa.status is "${baa.status}" with no verified_on date (YYYY-MM-DD)`);
      if (baa.status === "offered_on_tier" && !baa.tier) fail(where, `baa.status is "offered_on_tier" but no tier is named`);
    }
    if (baa.status === "unverified" && (baa.source_url || baa.verified_on)) {
      warn(where, "carries a source or a date but is still marked unverified — did someone forget to flip the status?");
    }
    if (baa.verified_on && ISO_DATE.test(baa.verified_on)) {
      const ageDays = (Date.now() - Date.parse(baa.verified_on)) / 86400000;
      if (ageDays > 365) warn(where, `BAA verified ${Math.floor(ageDays / 30)} months ago — worth re-checking before it goes in a report`);
    }

    // ——— pricing: same discipline, lower stakes ———
    const p = v.pricing ?? {};
    if (p.from_usd_month !== null && !(typeof p.from_usd_month === "number" && p.from_usd_month >= 0)) {
      fail(where, "pricing.from_usd_month must be a non-negative number or null");
    }
    if (typeof p.from_usd_month === "number" && !ISO_DATE.test(p.checked_on ?? "")) {
      fail(where, "pricing has a number but no checked_on date — prices move");
    }

    if (v.setup?.effort && !EFFORT.includes(v.setup.effort)) {
      fail(where, `setup.effort "${v.setup.effort}" is not one of: ${EFFORT.join(", ")}`);
    }
    if (v.setup?.effort === "needs-a-developer") {
      warn(where, 'marked "needs-a-developer" — per the report rules this should not reach a practice recommendation');
    }
  }
}

const verified = (data.vendors ?? []).filter((v) => v.baa?.status !== "unverified").length;
const total = (data.vendors ?? []).length;

for (const w of warnings) console.warn(`  warn  ${w}`);
for (const e of errors) console.error(`  ERROR ${e}`);

console.log(
  `\n${total} vendors · ${verified} with a verified BAA position · ` +
  `${errors.length} error${errors.length === 1 ? "" : "s"}, ${warnings.length} warning${warnings.length === 1 ? "" : "s"}`
);

if (errors.length) process.exit(1);
