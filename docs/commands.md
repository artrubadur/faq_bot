# Custom Command System

The system allows creating custom commands without writing code. Commands are defined in the configuration file using `key: value` format, where the key is the command name and the value is the bot's response.

YOu can find simple example the [messages.example.yml](../config/messages.example.yml), which fully represents default values.

## Multiline Commands

For longer responses, use the multiline syntax with `|` or `>` character:

```yaml
commands:
  # `|` - Preserves line breaks
  info: |
    Line 1
    Line 2
  # Result:
  # Line 1
  # Line 2

  # `>` - Folds into one line
  help: >
    Line 1
    Line 2
  # Result: Line 1 Line 2 Line 3
```

### Variables

All [message fields](messages.md#message-context-variables) are available in custom commands:

```yaml
commands:
  profile: |
    👤 Your Profile:
    ID: {id}
    Name: {first_name}
    Username: {username}
    
  time: "Current time: {date}"
```