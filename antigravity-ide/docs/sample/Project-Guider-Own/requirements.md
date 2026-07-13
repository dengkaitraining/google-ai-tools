# 需求文件 (requirements.md) - 將專案 Rule 與 Workflow 生成為 Skill

## 1. 專案目標與背景 (Project Goal)
目前專案中定義了助教的引導規則 (`.agents/rules/`) 與三階段的工作流 (`.agents/workflows/`)。
為了解耦並提升複用性，我們需要將本專案的 Rules 與 Workflows 蒸餾並封裝成一個自訂技能 (Custom Skill)，命名為 `project-guider`。
這能讓該技能在其他專案或全域環境中被載入與使用，同時不影響此專案現有的運行。

## 2. 功能性需求 (Functional Requirements)
1. **建立 Skill 目錄結構**：
   - 在 `.agents/` 底下建立 `skills/project-guider/` 資料夾。
   - 在該目錄下建立 `references/` 子資料夾。
2. **撰寫核心 SKILL.md**：
   - 必須包含 YAML Frontmatter，例如：
     ```yaml
     name: project-guider
     description: 軟體開發助教引導工具，負責引導學生描述需求、制定計畫、追蹤任務與驗證交付，並嚴格監督四大文件（requirements.md, implementation_plan.md, task.md, walkthrough.md）的更新與確認。
     ```
   - 內文說明 Skill 的定位、扮演的助教角色，以及如何使用參考文件中的 Workflows。
3. **複製 Rules 與 Workflows 到 Skill 的 references/ 目錄**：
   - 將以下檔案複製至 `.agents/skills/project-guider/references/` 下：
     - [guide-rule.md](file:///home/dengkai/projects/google-ai-tools/antigravity-ide/docs/sample/Project-Guider-Own/.agents/rules/guide-rule.md)
     - [project-rule.md](file:///home/dengkai/projects/google-ai-tools/antigravity-ide/docs/sample/Project-Guider-Own/.agents/rules/project-rule.md)
     - [edu-start.md](file:///home/dengkai/projects/google-ai-tools/antigravity-ide/docs/sample/Project-Guider-Own/.agents/workflows/edu-start.md)
     - [edu-plan.md](file:///home/dengkai/projects/google-ai-tools/antigravity-ide/docs/sample/Project-Guider-Own/.agents/workflows/edu-plan.md)
     - [edu-verify.md](file:///home/dengkai/projects/google-ai-tools/antigravity-ide/docs/sample/Project-Guider-Own/.agents/workflows/edu-verify.md)
4. **保留專案原有的檔案結構**：
   - 保持原有的 `.agents/rules/` 與 `.agents/workflows/` 目錄不變，確保在此專案中繼續使用斜線指令不受影響。

## 3. 技術要求 (Technical Requirements)
- 新增 Skill 目錄：`.agents/skills/project-guider/`
- 主要文件：`SKILL.md`
- 參考文件放置處：`references/`

## 4. 使用者情境 (User Scenarios)
- **情境：載入 Skill**
  當 Agent 載入 `project-guider` 技能時，能自動理解自己扮演「耐心軟體開發助教」的角色，並得知有哪三個階段的 workflows 以及四大文件的規範。
