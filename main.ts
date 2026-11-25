import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir: string = dirname(fileURLToPath(import.meta.url));
const sourcePath: string = join(scriptDir, "entry.png");

const envOutputDir: string | undefined = process.env.MAKEFUN_OUTPUT_DIR;
const outputDir: string = envOutputDir && envOutputDir.trim().length > 0 ? envOutputDir : "/output";
const destPath: string = join(outputDir, "entry.png");

mkdirSync(outputDir, { recursive: true });
copyFileSync(sourcePath, destPath);

process.stdout.write("Copied " + sourcePath + " to " + destPath + "\n");
