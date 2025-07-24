{% macro test_expression_is_true(model) %}
  {% set expression = kwargs.get('expression') %}

  {% if not expression %}
    {{ exceptions.raise_compiler_error("El argumento 'expression' es requerido para el test expression_is_true.") }}
  {% endif %}

  select 1
  from {{ model }}
  where not({{ expression }})
{% endmacro %}