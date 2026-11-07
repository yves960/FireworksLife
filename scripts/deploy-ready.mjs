#!/usr/bin/env node
/**
 * deploy-ready —— owner login 后的一键上线链（蔚 11-07 工单#3）。
 *
 * 串联：netlify status（登录检查）→ 建站/关联 fireworkslife → 首部署（--prod，
 * 走根目录 netlify.toml：cd frontend && build）→ frontend/scripts/verify-live 七项验收。
 * owner 唯一前置：终端跑一次 `netlify login`（30 秒）。本脚本任何一步失败即停，
 * 不半推半就。
 */
import { spawnSync } from "node:child_process";
import { existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const SITE_NAME = "fireworkslife";

const run = (title, command, args, opts = {}) => {
  console.log(`\n== ${title} ==\n$ ${command} ${args.join(" ")}`);
  const result = spawnSync(command, args, { stdio: "inherit", cwd: opts.cwd ?? ROOT, env: process.env });
  if (result.status !== 0) {
    console.error(`[deploy:ready] ✗ ${title} 失败（exit ${result.status}）——链路终止，后续步骤未执行`);
    process.exit(result.status ?? 1);
  }
  return result;
};

// 0) 前置：netlify CLI 在不在
const which = spawnSync("which", ["netlify"], { encoding: "utf8" });
if (which.status !== 0 || !which.stdout.trim()) {
  console.error("[deploy:ready] ✗ 未找到 netlify CLI——先 `npm install -g netlify-cli`，再 `netlify login`（owner 30 秒动作）");
  process.exit(1);
}

// 1) 登录检查：status 未登录会非零退出
const status = spawnSync("netlify", ["status"], { encoding: "utf8", cwd: ROOT });
if (status.status !== 0) {
  console.error("[deploy:ready] ✗ 未登录或未关联——owner 请先跑 `netlify login`（浏览器授权 30 秒），再重跑本命令");
  process.exit(1);
}
console.log("[deploy:ready] ✓ 已登录，开始建站/关联");

// 2) 建站（已存在则失败）→ 兜底按名关联
const created = spawnSync("netlify", ["sites:create", "--name", SITE_NAME], { encoding: "utf8", cwd: ROOT });
if (created.status === 0) {
  console.log(`[deploy:ready] ✓ 站点 ${SITE_NAME}.netlify.app 已创建`);
} else {
  run(`关联既有站点 ${SITE_NAME}`, "netlify", ["link", "--name", SITE_NAME]);
}

// 3) 首部署（--prod；netlify.toml 在根目录，publish=frontend/dist）
run("首部署 --prod", "netlify", ["deploy", "--prod"]);

// 4) 七项验收（打线上）
const verify = join(ROOT, "frontend", "scripts", "verify-live.mjs");
if (!existsSync(verify)) {
  console.error("[deploy:ready] ✗ 找不到 frontend/scripts/verify-live.mjs");
  process.exit(1);
}
run("上线七项验收 verify-live", process.execPath, [verify]);

console.log(`\n[deploy:ready] 🎉 ${SITE_NAME}.netlify.app 上线全链完成（部署 + 验收全绿）`);
