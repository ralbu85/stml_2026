# Week 3 — Implementation companion for the later lab

This optional reference contains interface details removed from the concept briefing. Read it alongside [W3_lab_tools.ipynb](../W3_lab_tools.ipynb), after the lecture. Examples use the Chat Completions interface; field names and provider controls are implementation choices, not definitions of tool-use intelligence.

The conceptual lecture covers selection, request formation, external execution, observations, and learning. The lab connects these concepts to concrete messages, validation, and execution records.

## Tool definition and executable implementation

A tool definition specifies a name, a natural-language description, and an input schema. The implementation provides the executable behavior.

EXAMPLE · forecast tool definition

```text
Name: get_forecast
Description: Retrieve a forecast for an explicitly specified city.
Input schema: city is a string; day is today or tomorrow.
Implementation: query the forecast service and return its response.
```

The description guides selection and interpretation. The input schema specifies accepted structure; the implementation determines execution.

The input schema can itself contain natural-language property descriptions. Description and schema are not disjoint technologies: structured constraints and semantic explanations coexist within a tool definition.

Sources: [OpenAI · Function calling](https://developers.openai.com/api/docs/guides/function-calling)

## Parameters and arguments

A parameter is a named input variable declared in a function interface. An argument is a value supplied for that parameter in a particular call.

EXAMPLE · parameter–argument mapping

```text
Interface: get_forecast(city: string, day: string)
Request: get_forecast(city="Seoul", day="tomorrow")
Parameter–argument mappings: city → "Seoul"; day → "tomorrow"
```

The declaration describes permitted inputs; the request instantiates them. Request generation does not invoke the executable implementation.

Sources: [OpenAI · Function calling](https://developers.openai.com/api/docs/guides/function-calling)

## Input schema and parameter constraints

An input schema declares the structure and constraints of a request. This JSON Schema requires both parameters and excludes undeclared fields.

EXAMPLE · input JSON Schema

```text
{"type":"object",
 "properties":{
   "city":{"type":"string"},
   "day":{"type":"string","enum":["today","tomorrow"]}},
 "required":["city","day"],
 "additionalProperties":false}
```

properties declares inputs; required lists mandatory fields; enum restricts allowed values. additionalProperties:false rejects undeclared fields.

This is the complete input-schema object for the example, not a complete API request. A full tool definition also supplies the function name and description. Natural-language descriptions may further state geographic interpretation, time basis, output fields, and limitations.

Sources: [OpenAI · Function calling](https://developers.openai.com/api/docs/guides/function-calling); [OpenAI · Structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs)

## Function calling and request representation

Function calling is an API mechanism that represents model-generated operation requests in designated structured fields.

EXAMPLE · Chat Completions request

```text
Chat Completions tool-call entry (illustrative):
{"id":"call_1", "type":"function",
 "function":{"name":"get_forecast",
 "arguments":"{\"city\":\"Seoul\",\"day\":\"tomorrow\"}"}}
```

The name identifies the operation; arguments contains JSON-encoded input values. The identifier associates the request with its later result.

This example uses Chat Completions serialization to match the Week 3 manual API demonstration. Other APIs can encode equivalent requests differently. Valid JSON encoding alone does not establish schema conformance or task correctness.

Sources: [OpenAI · Function calling](https://developers.openai.com/api/docs/guides/function-calling)

## Model selection and application constraints

Instructions influence generation; API settings constrain the permitted choices.

EXAMPLE · instruction and API controls

```text
Instruction: "Retrieve the forecast before answering."
auto: direct answer or tool request
required: one or more tool requests
forced function: request the specified function
none: no tool request
```

Request selection, argument validity, and execution success are separate properties.

For a forced function, Chat Completions uses {"type":"function","function":{"name":"get_forecast"}}. Parallel tool-call settings are separate from tool_choice. A prompt can influence behavior without providing the same API-level constraint.

Sources: [OpenAI · Function calling](https://developers.openai.com/api/docs/guides/function-calling)

## Structural validity and task correctness

Structural validity is conformity to the declared input schema. Task correctness is agreement between the requested operation and the user’s objective.

EXAMPLE · valid structure, incorrect city

```text
User request: retrieve tomorrow’s forecast for Seoul.
Arguments: {"city":"Busan", "day":"tomorrow"}
Schema check: valid. Task check: incorrect city.
```

Schema constraints validate representation; they cannot establish that the request satisfies the task. Strict schema adherence does not imply semantic correctness.

Sources: [OpenAI · Structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs); [Anthropic · Writing effective tools](https://www.anthropic.com/engineering/writing-tools-for-agents)

## Request validation and tool execution

Request validation checks the operation, input constraints, and applicable permissions before dispatch to the implementation.

EXAMPLE · validated forecast execution

```text
Registered function: get_forecast
Validated arguments: {"city":"Seoul", "day":"tomorrow"}
Execution: forecast service query
Result: Seoul, tomorrow: rain is forecast.
```

The result is hypothetical. The service query, rather than the generated request, produces the forecast observation.

Sources: [OpenAI · Function calling](https://developers.openai.com/api/docs/guides/function-calling)

## Result association and context update

A result message associates returned data with a prior request. The application preserves that request and adds its result to the next model input.

EXAMPLE · result message

```text
Chat Completions result message (illustrative):
{"role":"tool", "tool_call_id":"call_1",
 "content":"Seoul, tomorrow: rain is forecast."}
```

tool_call_id identifies the corresponding request. Subsequent generation is conditioned on the expanded conversation, including the returned evidence.

 The content field serializes the same service result as text. Its representation changes neither the forecast nor the request identity.

Sources: [OpenAI · Function calling](https://developers.openai.com/api/docs/guides/function-calling)

## Validation failure and diagnostic feedback

A validation failure occurs when a request violates input or permission constraints before the operation is executed.

EXAMPLE · rejected date argument

```text
Request: get_forecast(city="Seoul", day="next Friday")
Diagnostic: day must be today or tomorrow.
Execution status: forecast service not invoked.
Subsequent answer: The available tool does not support the requested date.
```

Diagnostic feedback can inform a corrected request or an explanation of the limitation. Substituting a different date would change the task.

## Execution failure and uncertain outcomes

An execution failure occurs after an accepted request is dispatched. A timeout can leave the operation’s outcome unknown.

EXAMPLE · service timeout

```text
Accepted request: get_forecast("Seoul", "tomorrow")
Execution outcome: service response timed out.
Available evidence: no forecast received.
```

The application may report the failure or apply a bounded retry policy. A missing response supplies no weather premise for the final answer.

Validation errors and execution failures occur at different stages. A timeout on a state-changing operation is especially important: the operation might have completed even though its response was lost. Retrying then requires a duplicate-prevention or status-check strategy.

Sources: [Anthropic · Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)

## State consistency and duplicate prevention

State consistency requires a write operation to respect the current application state at execution time. A previous observation may become stale.

EXAMPLE · concurrent inventory change

```text
Stock lookup: one coat available.
Concurrent event: another customer reserves that coat.
Reservation execution: reject because current stock is unavailable.
```

For retries, an idempotency key identifies the same logical request so the service can avoid duplicate effects. Completion still requires execution evidence.

An idempotent operation has the same intended effect when repeated as when executed once. An idempotency key can let a service recognize a repeated submission. Availability checks and inventory updates must be coordinated by the implementation, not inferred from an earlier model-visible observation.

Sources: [AWS Builders’ Library · Idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)
