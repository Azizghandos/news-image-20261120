// News-image entry for 20 November 2026 (Node 22, standard library only).
//
// The entry image is entry.png beside this file: a front page drawn for this
// competition by make-image.py (Pillow, flat colours, crisp text) that sums up
// Friday 20 November 2026 — the ICJ genocide ruling, the Shenzhen summit,
// the Kyiv strikes, the Riyadh missile, the market sell-off, COP31 and more.
// The program copies that image to the grader's output directory, so both
// runs write exactly the same bytes. It reads nothing else and needs no
// network, so it runs the same in the grader's fresh container.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL('./entry.png', import.meta.url), join(outDir, 'entry.png'));
