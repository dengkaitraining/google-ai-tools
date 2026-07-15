const fs = require('fs');
const path = require('path');

function toKebabCase(str) {
  return str
    .match(/[A-Z]{2,}(?=[A-Z][a-z]+[0-9]*|\b)|[A-Z]?[a-z]+[0-9]*|[A-Z]|[0-9]+/g)
    .map(x => x.toLowerCase())
    .join('-');
}

function generateScaffold(skillName, subFeatures, techStack) {
  const kebabName = toKebabCase(skillName);
  const targetDir = path.join(process.cwd(), '.agent', 'skills', kebabName);
  
  // 建立目錄結構
  fs.mkdirSync(targetDir, { recursive: true });
  fs.mkdirSync(path.join(targetDir, 'scripts'), { recursive: true });

  // 1. 寫入 SKILL.md (包含 YAML frontmatter 以符合 Agent Skill 規範)
  const skillMdContent = `---
name: ${kebabName}
description: Auto-generated skill for ${skillName}
---

# Skill: ${skillName}

## 核心功能
${subFeatures.map((f, i) => `${i + 1}. ${f}`).join('\n')}

## 參數規範 (Arguments Schema)
*(請在此處根據子功能定義對應的 JSON Schema)*
`;
  fs.writeFileSync(path.join(targetDir, 'SKILL.md'), skillMdContent, 'utf-8');

  // 2. 根據技術棧寫入相依性檔案與範例腳本
  if (techStack === 'python') {
    fs.writeFileSync(path.join(targetDir, 'requirements.txt'), '# 新增你的 Python 套件相依性，例如：\n# requests>=2.31.0\n', 'utf-8');
    fs.writeFileSync(path.join(targetDir, 'scripts', 'handler.py'), '#!/usr/bin/env python3\nimport sys\n\ndef main():\n    print("Skill initialized")\n\nif __name__ == "__main__":\n    main()\n', 'utf-8');
  } else {
    const pkgJson = {
      name: kebabName,
      version: "1.0.0",
      description: `Auto-generated skill for ${skillName}`,
      main: "scripts/handler.js",
      dependencies: {}
    };
    fs.writeFileSync(path.join(targetDir, 'package.json'), JSON.stringify(pkgJson, null, 2), 'utf-8');
    fs.writeFileSync(path.join(targetDir, 'scripts', 'handler.js'), '//@ts-check\nconsole.log("Skill initialized");\n', 'utf-8');
  }

  console.log(`[Success] Skill '${kebabName}' scaffolded successfully at: ${targetDir}`);
}

// 範例執行（Agent 內部調用實際行為）
const args = process.argv.slice(2);
if (args.length >= 3) {
  const [name, featuresStr, stack] = args;
  generateScaffold(name, JSON.parse(featuresStr), stack);
}
