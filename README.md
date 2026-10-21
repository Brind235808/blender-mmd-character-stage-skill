# Character Stage for Blender/MMD · Blender/MMD 角色场景搭建 Skill

[中文](#中文) | [English](#english)

A reusable Qoder-style skill that stages a Blender/MMD character from just a model or reference images: reads the character's style, builds the set, lighting, camera, atmosphere and compositor, then iterates headlessly with saved versions and delivers a packed, portable scene.

一个可复用的 Qoder skill：只提供角色模型或角色图片，就会按角色风格自动搭建场景、灯光、镜头、雾与后期，全程后台渲染、逐版保存并打包交付。

- Entry / 入口：[SKILL.md](SKILL.md)
- Version / 版本：`v1.0.0` · 2026-10-21

---

## 中文

### 范围

**包含**：角色导入与落地、风格分析、布景、分层灯光、相机与景深、雾与后期、后台截图迭代、版本记录、贴图打包与迁移交付。

**不包含**：角色着色器重制、角色材质替换/重新贴图、动作或动画制作、模型配布。黑棚舞台只作为场景/灯光案例，不涉及着色器。

### 工作流

1. **角色准备**：PMX/FBX 导入、身高归一、落地、朝向、姿势、成人配件隐藏、眼睛对焦点。
2. **风格卡**：发色/瞳色/服装/材质/轮廓/题材/叙事，映射到场景方向。
3. **镜头先行**：先定构图和机位，再决定布景，只建镜头能看到的东西。
4. **布景**：一个主场景 + 2–3 个道具 + 接地阴影，材质和比例可信。
5. **分层灯光**：主光 → 补光 → 轮廓 → 背景 → 实用光源 → 雾。
6. **相机/景深**：全身 44–50mm，三分之四身 65–85mm，近景 85–105mm；对焦在眼球表面。
7. **氛围/后期**：体积雾、Fog Glow、色彩平衡、暗角、镜头畸变。
8. **后台迭代**：先保存 `versions/vNN_scene.blend`，低分辨率预览，检查截图，每次只改一组变量。
9. **交付**：打包贴图、相对输出路径、校验、版本对照表、最佳图 + 对应 `.blend`、备份。

详细方法：

- [角色准备](references/character-prep.md)
- [灯光配方](references/lighting-recipes.md)
- [调试手册](references/scene-debug-playbook.md)
- [完整案例](references/case-studies.md)
- [用户提示词与交付规则](references/user-brief.md)

### 安装

Windows PowerShell：

```powershell
git clone https://github.com/Brind235808/blender-mmd-character-stage-skill.git "$env:USERPROFILE\.qoder-cn\skills\build-character-stage"
```

Bash：

```bash
git clone https://github.com/Brind235808/blender-mmd-character-stage-skill.git ~/.qoder-cn/skills/build-character-stage
```

然后重启会话或执行 `/skills reload`，用 `/build-character-stage` 调用。更新时在 skill 目录执行 `git pull`。

### 使用

```text
/build-character-stage 角色：D:\path\character.pmx
按角色气质搭一个室内场景，后台渲染；每个版本先保存再改进，最后打包交付。
```

只提供角色图片也可以，skill 会先做风格卡，再决定布景和灯位。角色模型、贴图和参考图不会上传到本仓库。

### 目录

```text
.
├─ SKILL.md
├─ README.md
├─ references/
│  ├─ character-prep.md
│  ├─ lighting-recipes.md
│  ├─ scene-debug-playbook.md
│  ├─ case-studies.md
│  └─ user-brief.md
└─ scripts/
   ├─ inspect_blend.py
   ├─ render_preview.py
   ├─ verify_pack.py
   └─ contact_sheet.py
```

### 脚本

| 脚本 | 作用 |
|---|---|
| `inspect_blend.py` | 后台读取场景、灯光、相机、世界、贴图打包状态、输出路径 |
| `render_preview.py` | 后台预览渲染，可覆盖分辨率/采样；`--raw`、`--no-fog`、`--no-bloom` 用于排障 |
| `verify_pack.py` | 检查贴图是否全部打包、0 缺失、相对输出路径、相机和分辨率；失败时非 0 退出 |
| `contact_sheet.py` | 用 Pillow 生成带版本标签的对照表，支持中文标题 |

所有 Blender 脚本都以 `blender.exe -b --python ...` 运行，不会弹出前台窗口。需要 Blender 3.6.x（EEVEE Legacy；4.2+ 的 EEVEE Next 会改变 Bloom/SSR/体积光表现）、PMX 需 MMD Tools；对照表需要 Python 3 + Pillow。

### 已验证

- 在已打包的 v11（97/97 贴图）和 v23（41/41 贴图）成品上实测。
- `verify_pack.py` 对三份成品全部 PASS，0 缺失，相对路径正确。
- `render_preview.py` 真实渲染出图；`contact_sheet.py` 中文标题和 BEST 标记正常。
- 不包含任何模型、贴图、渲染图或参考图。

### 授权

本仓库只包含 skill 文本和辅助脚本，不包含模型、贴图、渲染图或参考图。角色模型仍受其原始授权约束；若模型 readme 禁止二次配布，请勿上传或分享包含模型数据的 `.blend`。

---

## English

### What it is

A reusable skill for building a **character-first scene** in Blender/MMD. Given a character model (PMX/FBX/GLB) or character images, it derives a style card, chooses a scene direction, builds the set, layers the lights, sets the camera/DOF, adds atmosphere and compositor effects, and iterates with headless previews.

### Scope

**Included:** character import and staging, height/ground/facing, eye focus, style analysis, set dressing, layered lighting, camera/DOF, fog/compositor, headless preview iteration, version saving, texture packing, and portable delivery.

**Excluded:** character shader authoring, material replacement/re-texturing, animation, and model redistribution. The black studio is included only as a scene/lighting case, with no shader work.

### Workflow

1. Prepare the character: import, normalize height, ground the feet, face the camera, hide adult add-ons, measure the eye focus point.
2. Read the style: palette, materials, silhouette, genre, narrative beat → scene direction.
3. Compose camera-first: choose framing and one hero prop before building the room.
4. Build the set: a simple interior/stage, 2–3 supporting props, contact shadow.
5. Light in layers: key → fill → rims → background → practicals → atmosphere.
6. Camera/DOF: 44–50 mm full body, 65–85 mm three-quarter, 85–105 mm close-up; focus on the eye surface.
7. Atmosphere/compositor: volumetric fog, Fog Glow, color balance, vignette, lens distortion.
8. Iterate headlessly: save `versions/vNN_scene.blend` before each render, preview at low resolution, inspect the PNG, change one variable group.
9. Deliver: pack textures, use `//renders/...` paths, verify, contact sheet, best image + matching `.blend`, backup.

Deep dives: [character prep](references/character-prep.md), [lighting recipes](references/lighting-recipes.md), [debug playbook](references/scene-debug-playbook.md), [case studies](references/case-studies.md), [user brief](references/user-brief.md).

### Install

```bash
git clone https://github.com/Brind235808/blender-mmd-character-stage-skill.git ~/.qoder-cn/skills/build-character-stage
```

On Windows PowerShell, clone into `$env:USERPROFILE\.qoder-cn\skills\build-character-stage`. Restart the session or run `/skills reload`, then invoke `/build-character-stage`.

### Usage

```text
/build-character-stage character: D:\path\character.pmx
Build a scene that fits the character, render headlessly, save each version before improving it,
and deliver a packed project.
```

### Scripts

- `inspect_blend.py` — scene, lights, camera, world, images, pack status, output path.
- `render_preview.py` — headless preview with resolution/sample overrides; `--raw`, `--no-fog`, `--no-bloom` for diagnosis.
- `verify_pack.py` — packed textures, missing images, relative output path, camera, resolution; exits nonzero on failure.
- `contact_sheet.py` — labeled version sheet with Pillow, optional Chinese title and BEST marker.

Requirements: Blender 3.6.x with EEVEE Legacy (4.2+ changes bloom/SSR/volume behavior), MMD Tools for PMX, Python 3 + Pillow for the contact sheet.

### Verified

Tested on the packed v11 and v23 deliverables: 97/97 and 41/41 textures, zero missing, relative output paths; preview renders and the contact sheet were run for real. No model, texture, render, or reference image is included.

### License

This repository contains only skill text and helper scripts. No character model, texture, render, or reference image is included. Character assets remain under their original licenses; if the model readme forbids redistribution, keep any `.blend` containing model data local.
