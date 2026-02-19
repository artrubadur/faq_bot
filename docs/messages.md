# String Customization System
## 0. Overview

This system provides a flexible mechanism for customizing all text strings used by the bot. Its primary purpose is **localization**, but it can also be used for other purposes such as:
- Rebranding (changing terminology)
- Adjusting tone and style
- Quick text edits without code changes

Field descriptions can be found in the [messages.example.yml](../config/messages.example.yml), which fully represents default values. **Note: The original default values apply emojis directly, you don't need `constants.example.yml` for launching without `messages.example.yml`.**

## 1. Dynamic Variable Substitution
All strings support dynamic variable insertion using curly braces `{variable_name}`. Variables are automatically replaced with actual values at runtime.

**Example:**
```yaml
start: "Hello, {first_name}! I will help you find the answer"
```
When sent to a user named John, becomes: "Hello, John! I will help you find the answer"

## 2. Formatting Modes
The `parse_mode` setting at the top of the file controls how text* is formatted:
- `html` - Supports HTML tags
- `markdown` - Supports Markdown formatting
- `None` - Plain text only

Here's a comprehensive comparison table of HTML and Markdown formatting syntax based on the provided classes:

| Decoration | HTML | MarkDown | Result |
|------------|------|----------|--------|
| **Bold** | `<b>text</b>` | `**text**` | **text** |
| **Italic** | `<i>text</i>` | `*text*` | *text* |
| **Underline** | `<u>text</u>` | `__text__` | <u>text</u> |
| **Strikethrough** | `<s>text</s>` | `~text~` | ~~text~~ |
| **Spoiler** | `<tg-spoiler>text</tg-spoiler>` | `\|\|text\|\|` | ❄❄❄❄ |
| **Code** | `<code>code</code>` | \`text\` | `code` |
| **Pre (Code Block)** | `<pre>code</pre>` | \r```code```` | \```code```
| **Pre with Language** | `<pre><code class="language-python">code</code></pre>` | \```\ntext\n\``` | ```
| **Blockquote** | `<blockquote>line_1`<br>`line_2</blockquote>` | `>line_1`<br>`>line_2` | > line_1<br>> line_2 |
| **Expandable Blockquote** | `<blockquote expandable>line_1`<br>`line_2</blockquote>` | `>line_1`<br>`>line_2\|\|` | > line_1<br>> line_2 \|\| |
| **Link** | `<a href="https://text.ru">text</a>`<br> | `[text](https://text.ru)` | [text](https://example.com) |
| **Mention/User or Channel Link** | `<a href="link**">@text</a>`<br>`<a href="link**">line_2</a>` | - | @text |
| **Custom Emoji** | `<tg-emoji emoji-id="123"></tg-emoji>` | `![text](tg://emoji?id=123)` | (custom emoji) |

### Notes:
* *The parse mode also applies to [custom commands](commands.md).
* **Possible mention links:
  * `tg://user?id=*id*`
  * `https://t.me/*user_or_channel_name*`

## 3. Variable Documentation

The system supports dynamic variable interpolation in text templates. Variables are enclosed in curly braces `{}` and are replaced with appropriate values at runtime.

**Example:** `Hello, {first_name}!` will be replaced with the user's actual first name.

### Message Context Variables

The `message` variable is automatically available in all public message responses and contains the following user information:

- `id` - Telegram user ID
- `first_name` - User's first name
- `last_name` - User's last name (may be empty)
- `username` - Telegram username (may be empty)
- `full_name` - Combined first and last name
- `date` - Message date in format passed to `format.field.date`

This applies only to the predefined public user interface (`responses.public`) and [custom commands](commands.md).

### Identity Variable

The `identity` variable represents a user identifier - it returns the username if available, otherwise falls back to the user ID. Used primarily in error messages and user references.

**Example:** `User {identity} not found` might become "User @john_doe not found" or "User 123456789 not found".

### Passed Variables

Comments with `< variable` indicate which variables are passed to that specific message:

```yaml
successful: | # < user
  {emoji.status.successful} User created:
  {user}
```

In this example, the `user` variable (containing formatted user data) is available in the message.

### Entity Formatting

Two main entities support structured formatting:

- `user` - Formatted using `format.user` template
- `question` - Formatted using `format.question` template

Individual fields within these entities are formatted using `format.field` templates:

```yaml
user: # Complete user representation
  id: "ID: {id}" # Uses format.field.id for the {id} part
  username: "Username {username}" # Uses format.field.username for {username}
```

If a value passed to `format.field` is empty, the system falls back to `format.fallback` for that field.

### Button Variables

Buttons use the `button.*` namespace and have their own variable handling:

```yaml
button:
  user:
    found: "Found ({identity})" # < identity
```

Note: **`button.*` does not apply `format.field` formatting** - button text uses raw variable substitution only.

### Constants

Constants are predefined values (e.g. emojis) defined in the configuration. **Important: Constants are resolved only once during system initialization and never change during runtime.** They can be referenced using dot notation:

**Examples:**
- `{emoji.status.successful}` 
- `{your.service.name}`

Since constants are immutable after initialization, they provide consistent visual elements throughout the entire application lifecycle.

### Variable Resolution and Errors

When resolving a variable, the system checks in this order:
1. Constants (defined in the configuration and frozen at initialization)
2. Runtime variables (passed to the specific message)

If a variable does not exist in either runtime variables or constants, the system will raise an error. Constants cannot 

If a variable does not exist in either runtime variables or constants, the system will raise an error. **Constants cannot override runtime variables** . The following reserved names cannot be used as constant names at the first nesting level as they would conflict with runtime variables: `identity`, `id`, `user`, `first_name`, `last_name`, `username`, `full_name`, `date`, `user_link`, `user_role`, `question`, `question_text`, `answer_text`, `rating`, `old`, `new`, `page`, `max_page`, `content`, `exception`.

## 4. Routing

### Error Message Routing
Error messages are routed through different response channels depending on their source:

- **`exceptions.search.not_found`** - Passed through `responses.public.failed` and shown to regular users when a search fails
- **All other exceptions** - Passed through `responses.admin.invalid` and shown to administrators during operations

### Validation Message Context

Validation messages can appear in different contexts:

- **`validation.question.question_text_long`** - Can be sent through either `failed` (for public users) or `invalid` (for administrators) depending on who triggered the validation

### Question Input Processing Errors

Question input validation has two specific error messages:

- **`process.question.msg_question_text_invalid`** - Raised when a user sends a non-textual message (e.g., photo, video, sticker) instead of a text question
- **`process.question.cmd_question_text_invalid`** - Raised when a user sends a command with an empty prompt (e.g., just `/ask` without any question text)