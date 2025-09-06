# 样式文件组织结构

本项目已将前端样式代码从各个Vue组件中提取到独立的SCSS文件中，以提高代码的可维护性和复用性。

## 文件结构

```
src/styles/
├── index.scss          # 主样式文件（使用@use导入所有其他样式模块）
├── global.scss         # 全局样式、CSS变量、通用动画和工具类
├── layout.scss         # 布局样式（头部、底部、主内容区域）
├── element-plus.scss   # Element Plus组件样式覆盖
├── home.scss           # 首页专用样式
└── create.scss         # 创作页面专用样式
```

## 样式文件说明

### global.scss
- CSS变量定义（浅色/深色主题）
- 全局重置样式
- 滚动条美化
- 通用动画（spin, float, blink）
- 通用工具类（.spinning, .mr-2, .text-center, .cursor-indicator）

### layout.scss
- 应用程序布局容器样式
- 头部导航样式（logo、导航链接、主题切换按钮）
- 主内容区域样式
- 底部样式
- 响应式布局适配

### element-plus.scss
- Element Plus组件的主题适配样式
- 按钮、卡片、输入框、下拉菜单等组件的自定义样式
- 步骤条、消息提示、标签等组件的主题覆盖
- 加载指示器样式

### home.scss
- 首页英雄区域样式
- 浮动装饰元素动画
- 功能特色卡片样式
- 快速开始区域样式
- 响应式适配

### create.scss
- 创作页面布局样式
- 步骤指示器容器样式
- 表单卡片样式
- 流式生成容器样式
- 章节选择和结果展示样式
- 响应式适配

## 使用方式

样式文件通过 `src/styles/index.scss` 统一导入，并在 `main.ts` 中引入：

```typescript
// main.ts
import './styles/index.scss'
```

**注意：** 本项目使用现代化的 Sass `@use` 规则替代了已弃用的 `@import` 规则，以确保与 Dart Sass 3.0+ 的兼容性。

## 主题系统

项目使用CSS变量实现主题切换：
- 浅色模式：`:root` 选择器定义变量
- 深色模式：`[data-theme="dark"]` 选择器覆盖变量

## 命名规范

- 使用语义化的类名
- 遵循BEM命名规范
- CSS变量使用 `--` 前缀
- 动画使用 `@keyframes` 定义

## 响应式设计

所有样式都包含响应式适配：
- 768px以下：平板适配
- 480px以下：手机适配

## 维护建议

1. 新增页面样式时，创建对应的SCSS文件并在 `index.scss` 中导入
2. 通用样式放在 `global.scss` 中
3. 组件特定样式放在对应的页面样式文件中
4. Element Plus组件样式覆盖统一放在 `element-plus.scss` 中
5. 布局相关样式放在 `layout.scss` 中