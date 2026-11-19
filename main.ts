// Entry program for the gta6-meme-x-01 make.fun bounty (Node 22, stdlib only).
//
// The entry itself is a post on X: the house reads the post from X and
// judges its first picture and its text. This program's whole job is to
// hand the house the post's address: it copies POST.json from the
// repository root (MAKEFUN_BOT_DIR, '.' when run locally) into the
// output directory (MAKEFUN_OUTPUT_DIR), byte for byte, and stays
// silent on success.
//
// Local check:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

function envDir(name: string, fallback: string): string {
  const value = process.env[name];
  return value === undefined || value === "" ? fallback : value;
}

const sourceDir = envDir("MAKEFUN_BOT_DIR", ".");
const targetDir = envDir("MAKEFUN_OUTPUT_DIR", "out");

mkdirSync(targetDir, { recursive: true });
copyFileSync(join(sourceDir, "POST.json"), join(targetDir, "POST.json"));
