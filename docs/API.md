# co-novel API 文档

## 概述

本文档描述了co-novel项目中后端提供的所有API接口，包括接口地址、请求方法、参数和返回值。

## 基础URL

```
http://localhost:8000/api/ai
```

## 接口列表

### 1. AI服务健康检查

- **URL**: `/health`
- **方法**: `GET`
- **描述**: 检查AI服务的健康状态
- **请求参数**: 无
- **返回示例**:
```json
{
  "status": "healthy",
  "service": "AI"
}
```

### 2. 生成小说内容

- **URL**: `/generate-content`
- **方法**: `POST`
- **描述**: 根据提示词生成小说内容
- **请求参数**:
  - `prompt` (string, 必需): 生成内容的提示词
  - `max_tokens` (integer, 可选, 默认: 500): 最大生成token数
- **返回示例**:
```json
{
  "content": "生成的小说内容..."
}
```

### 3. 流式生成小说内容

- **URL**: `/generate-content-stream`
- **方法**: `POST`
- **描述**: 根据提示词流式生成小说内容（逐字显示）
- **请求参数**:
  - `prompt` (string, 必需): 生成内容的提示词
  - `max_tokens` (integer, 可选, 默认: 500): 最大生成token数
- **返回示例**:
```
这是生成的小说内容的第一部分...
这是生成的小说内容的第二部分...
```
- **注意**: 此接口返回的是流式数据，需要特殊处理以实现逐字显示效果。

### 4. 生成小说标题

- **URL**: `/generate-title`
- **方法**: `POST`
- **描述**: 根据小说类型和主题生成标题
- **请求参数**:
  - `genre` (string, 必需): 小说类型
  - `theme` (string, 必需): 小说主题
- **返回示例**:
```json
{
  "title": "《玄幻：魔法学院》"
}
```

### 5. 获取AI建议

- **URL**: `/suggestions`
- **方法**: `POST`
- **描述**: 根据当前内容获取AI建议
- **请求参数**:
  - `current_content` (string, 必需): 当前内容
  - `suggestion_type` (string, 必需): 建议类型（如：续写、修改、扩展等）
- **返回示例**:
```json
{
  "suggestions": "AI建议的内容..."
}
```

## 错误处理

所有API接口在发生错误时都会返回标准的JSON格式错误信息：

```json
{
  "error": "错误描述"
}
```

## 前端对接说明

前端应用需要通过HTTP请求调用上述API接口。建议使用axios库进行HTTP请求。

### 示例代码

```javascript
// 生成小说内容
const generateContent = async (prompt, maxTokens = 500) => {
  try {
    const response = await axios.post('/api/ai/generate-content', {
      prompt,
      max_tokens: maxTokens
    });
    return response.data.content;
  } catch (error) {
    console.error('生成内容失败:', error);
    throw error;
  }
};

// 生成小说标题
const generateTitle = async (genre, theme) => {
  try {
    const response = await axios.post('/api/ai/generate-title', {
      genre,
      theme
    });
    return response.data.title;
  } catch (error) {
    console.error('生成标题失败:', error);
    throw error;
  }
};

// 流式生成小说内容
const generateContentStream = async (prompt, maxTokens = 500) => {
  try {
    const response = await axios.post('/api/ai/generate-content-stream', {
      prompt: prompt,
      max_tokens: maxTokens
    }, {
      responseType: 'text'  // 重要：设置响应类型为text以处理流式数据
    });
    return response.data;  // 返回流式数据
  } catch (error) {
    console.error('流式生成内容失败:', error);
    throw error;
  }
};

// 生成小说内容（使用新API模型）
const generateContentWithModel = async (prompt, maxTokens = 500) => {
  try {
    const response = await axios.post('/api/ai/generate-content', {
      prompt: prompt,
      max_tokens: maxTokens
    });
    return response.data.content;
  } catch (error) {
    console.error('生成内容失败:', error);
    throw error;
  }
};

// 生成小说标题（使用新API模型）
const generateTitleWithModel = async (genre, theme) => {
  try {
    const response = await axios.post('/api/ai/generate-title', {
      genre: genre,
      theme: theme
    });
    return response.data.title;
  } catch (error) {
    console.error('生成标题失败:', error);
    throw error;
  }
};
```
