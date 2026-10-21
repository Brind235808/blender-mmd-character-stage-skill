# User Brief and Delivery Rules

This file preserves the user's original wording and the operating rules derived from it. Read it at the start of a new character-stage project, or when the user references "像之前那样".

## Original prompts (verbatim)

> 你能接入blender，帮我改渲染吗

> 我想做一个高质量mmd，你预估要多久，先策划一下怎么做，不要动手。

> 我这台电脑暂时没法套动作，但是有alicia的坎特蕾拉mmd模型，你自己找一下，吧光照，镜头背景，和渲染效果做好，场景你随便网上下一个比较简单的室内场景。然后开启目标模式，直到做好，做好之后对渲染结果截图，如果效果差，你就保存一份再改进，不要不保存

> 哦对了，你做的时候后台做，前台不要显示blender

> 我看了下，怎么只有图片文件，你把blender文件要保存一份到本地，然后把你做的几个版本的具体细节调整，记录一下，最后你决的最好的截图版本是哪个，那个要blender文件，然后你记得打包再保存，这样我换电脑也不会丢东西。

> 把前面做场景那部分总结为一个skill，后续我只要提供角色就能根据角色风格搭建灯光场景，调试细节和方法，还有我的提示词细节都写进skill，后面的角色渲染这方面不要，开始做一个skill

The last prompt defines this skill's scope: **scene, lighting, camera, atmosphere, debugging, delivery**. The later character-shader work (v13–v23 shader replacement) is intentionally out of scope.

## Derived rules

| Rule | Why / how to apply |
|---|---|
| **Plan first when asked** | If the user says "先策划一下，不要动手", produce a concrete plan and wait. Do not modify files. Otherwise proceed end-to-end. |
| **Goal-mode persistence** | Keep working until the scene is rendered, inspected, and delivered. Do not stop at "the script is ready" or "the plan is done". |
| **Headless Blender only** | Run `blender.exe -b --python <script>`. Never open the UI or leave a foreground Blender window. Background GPU/addon warnings are harmless. |
| **Save before improving** | Every iteration gets `versions/vNN_scene.blend` saved **before** rendering. Keep all old versions; never delete or overwrite them. |
| **Screenshot-driven iteration** | Render a preview PNG, inspect it visually, name the top three issues, fix them, repeat. A good log is not proof; the image is. |
| **Simple interior by default** | The user asked for a "比较简单的室内场景" from the web. Prefer one room, a few props, and lighting over a complex asset pile. Use CC0 assets (e.g. Poly Haven) when downloading. |
| **Local .blend files** | Save the project file, not only images. The `.blend` is the deliverable that can be reopened and re-rendered. |
| **Detailed version log** | Record each version's changes, parameters, and result; identify the best version and its matching `.blend`. |
| **Pack for moving computers** | `File > External Data > Pack Resources`, use relative render paths, verify zero missing textures, and create a backup. |
| **Do not disturb old deliverables** | New phase = new filenames (e.g. `_Shader_v23`, `_final_wide`); keep earlier best versions and old renders intact. |
| **Tasteful presentation** | If the model has adult/BDSM add-ons, hide them for a non-explicit render. Do not copy explicit poses from reference images; replicate lighting/scene language instead. |
| **Local-only license** | If the model readme forbids redistribution/resale/porting, never publish the `.blend` or model data. State this in the delivery note. |
| **Chinese updates** | The user writes Chinese; keep progress updates and the final summary in Chinese, concise and concrete. |

## Delivery checklist

- [ ] Best render PNG, full resolution, visually inspected.
- [ ] Matching `.blend`, saved and reopened to verify.
- [ ] All versions saved in `versions/`; all previews in `renders/`.
- [ ] Version log with: reference/style analysis, version table, final light/camera table, file list, usage, license.
- [ ] Contact sheet of versions.
- [ ] Textures packed; zero missing; output path starts with `//`.
- [ ] Backup archive containing the packed `.blend`, final renders, scripts, log, license.
- [ ] Final message: what changed, paths to best image + `.blend`, any known limitations.

## Suggested folder layout

```
project/
├─ versions/
│  ├─ v01_scene.blend
│  ├─ v02_scene.blend
│  └─ ...
├─ renders/
│  ├─ v01_preview.png
│  ├─ v02_preview.png
│  └─ ...
├─ scripts/
│  ├─ build_v01.py
│  ├─ build_v02.py
│  └─ ...
└─ deliverables/
   ├─ <Character>_final_wide.blend
   ├─ <Character>_final_closeup.blend
   ├─ renders/
   │  ├─ final_render.png
   │  ├─ final_closeup.png
   │  └─ version_contact_sheet.jpg
   ├─ scripts/
   ├─ license/
   │  └─ 模型授权说明_Readme.txt
   └─ 版本迭代记录.md
```

Use a new suffix when starting a new phase rather than overwriting the previous best:

- `Alicia_Cantarella_final_wide.blend` (Victorian scene)
- `Alicia_Cantarella_final_closeup.blend`
- `Alicia_Cantarella_Shader_v23.blend` (later phase; shader work is out of scope for this skill)

## Final report template (Chinese)

```
场景已完成，最佳版本 vNN。

关键改动：
- 布景：...
- 灯光：...
- 镜头：...
- 氛围/后期：...

成品：
- 成图：<path>
- 工程：<path>
- 版本记录：<path>
- 备份：<path>

限制：...
```

Keep it short; the version log carries the detail.
