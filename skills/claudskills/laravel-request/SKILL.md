---
name: laravel-request
description: Create Form Requests with validation rules, authorization, and custom error messages in Laravel 11+.
keywords: request, validation, form request, rules, authorize
---

# Laravel Request Skill

## Cuando Activar

- Usuario dice: "create request", "validation", "form request"
- Usuario necesita validar datos
- Usuario menciona rules o authorization

## Antes de Generar

**SIEMPRE pregunta:**

```
¿Qué necesitás validar?

1. Tipo de operación:
   - Store (crear) → campos requeridos
   - Update (actualizar) → campos opcionales
   
2. Campos:
   - ¿Cuáles son los campos?
   - ¿Tipos de datos? (string, int, enum, file)
   - ¿Validaciones especiales? (unique, exists, regex)

3. Authorization:
   - ¿Necesitás authorization? (policies)
   
4. Custom rules:
   - ¿Validaciones custom?

Contame para generar el request completo.
```

## Template - Store Request

```php
<?php

namespace App\Http\Requests;

use App\Enums\{{Model}}Status;
use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;

class Store{{Model}}Request extends FormRequest
{
    /**
     * Determine if the user is authorized to make this request.
     */
    public function authorize(): bool
    {
        // Check if user has permission
        return $this->user()->can('create', {{Model}}::class);
        
        // Or simply:
        // return true;
    }

    /**
     * Get the validation rules that apply to the request.
     */
    public function rules(): array
    {
        return [
            'name' => ['required', 'string', 'max:255'],
            'description' => ['nullable', 'string', 'max:1000'],
            'status' => ['required', Rule::enum({{Model}}Status::class)],
            'category_id' => ['required', 'integer', 'exists:categories,id'],
            'tags' => ['nullable', 'array'],
            'tags.*' => ['integer', 'exists:tags,id'],
            'image' => ['nullable', 'image', 'max:2048'], // 2MB max
            'is_featured' => ['boolean'],
            'price' => ['required', 'numeric', 'min:0', 'max:999999.99'],
            'published_at' => ['nullable', 'date', 'after:now'],
        ];
    }

    /**
     * Get custom attributes for validator errors.
     */
    public function attributes(): array
    {
        return [
            'name' => 'nombre',
            'description' => 'descripción',
            'status' => 'estado',
            'category_id' => 'categoría',
            'tags' => 'etiquetas',
            'image' => 'imagen',
            'is_featured' => 'destacado',
            'price' => 'precio',
            'published_at' => 'fecha de publicación',
        ];
    }

    /**
     * Get the error messages for the defined validation rules.
     */
    public function messages(): array
    {
        return [
            'name.required' => 'El nombre es obligatorio.',
            'name.max' => 'El nombre no puede exceder :max caracteres.',
            'status.required' => 'El estado es obligatorio.',
            'category_id.exists' => 'La categoría seleccionada no existe.',
            'price.min' => 'El precio debe ser mayor o igual a :min.',
            'image.image' => 'El archivo debe ser una imagen.',
            'image.max' => 'La imagen no puede exceder :max KB.',
            'published_at.after' => 'La fecha de publicación debe ser futura.',
        ];
    }

    /**
     * Prepare the data for validation.
     */
    protected function prepareForValidation(): void
    {
        $this->merge([
            'is_featured' => $this->boolean('is_featured'),
        ]);
    }

    /**
     * Get validated data with additional transformations.
     */
    public function validatedData(): array
    {
        $validated = $this->validated();

        // Transform data if needed
        if (isset($validated['price'])) {
            $validated['price'] = (float) $validated['price'];
        }

        return $validated;
    }
}
```

## Template - Update Request

```php
<?php

namespace App\Http\Requests;

use App\Enums\{{Model}}Status;
use App\Models\{{Model}};
use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;

class Update{{Model}}Request extends FormRequest
{
    /**
     * Determine if the user is authorized to make this request.
     */
    public function authorize(): bool
    {
        ${{model}} = $this->route('{{model}}');
        
        return $this->user()->can('update', ${{model}});
    }

    /**
     * Get the validation rules that apply to the request.
     */
    public function rules(): array
    {
        ${{model}} = $this->route('{{model}}');

        return [
            'name' => ['sometimes', 'string', 'max:255'],
            'description' => ['nullable', 'string', 'max:1000'],
            'status' => ['sometimes', Rule::enum({{Model}}Status::class)],
            'category_id' => ['sometimes', 'integer', 'exists:categories,id'],
            'tags' => ['nullable', 'array'],
            'tags.*' => ['integer', 'exists:tags,id'],
            'image' => ['nullable', 'image', 'max:2048'],
            'is_featured' => ['boolean'],
            'price' => ['sometimes', 'numeric', 'min:0', 'max:999999.99'],
        ];
    }

    /**
     * Get custom attributes for validator errors.
     */
    public function attributes(): array
    {
        return [
            'name' => 'nombre',
            'description' => 'descripción',
            'status' => 'estado',
            'category_id' => 'categoría',
            'price' => 'precio',
        ];
    }

    /**
     * Get the error messages for the defined validation rules.
     */
    public function messages(): array
    {
        return [
            'name.max' => 'El nombre no puede exceder :max caracteres.',
            'category_id.exists' => 'La categoría seleccionada no existe.',
            'price.min' => 'El precio debe ser mayor o igual a :min.',
            'image.max' => 'La imagen no puede exceder :max KB.',
        ];
    }
}
```

## Template - Custom Rule

```php
<?php

namespace App\Rules;

use Closure;
use Illuminate\Contracts\Validation\ValidationRule;

class ValidateSlug implements ValidationRule
{
    /**
     * Run the validation rule.
     */
    public function validate(string $attribute, mixed $value, Closure $fail): void
    {
        if (! preg_match('/^[a-z0-9]+(?:-[a-z0-9]+)*$/', $value)) {
            $fail('El :attribute debe ser un slug válido (solo letras minúsculas, números y guiones).');
        }
    }
}
```

```php
<?php

namespace App\Rules;

use Closure;
use Illuminate\Contracts\Validation\ValidationRule;

class MaxWords implements ValidationRule
{
    public function __construct(
        private readonly int $maxWords
    ) {}

    /**
     * Run the validation rule.
     */
    public function validate(string $attribute, mixed $value, Closure $fail): void
    {
        $wordCount = str_word_count($value);
        
        if ($wordCount > $this->maxWords) {
            $fail("El :attribute no puede exceder {$this->maxWords} palabras.");
        }
    }
}
```

## Validaciones Comunes

### Strings

```php
'name' => ['required', 'string', 'min:3', 'max:255'],
'slug' => ['required', 'string', 'alpha_dash', 'unique:{{table}},slug'],
'email' => ['required', 'email:rfc,dns', 'unique:users'],
'password' => ['required', 'string', 'min:8', 'confirmed'],
'url' => ['nullable', 'url', 'active_url'],
```

### Numbers

```php
'age' => ['required', 'integer', 'min:18', 'max:120'],
'price' => ['required', 'numeric', 'between:0.01,999999.99'],
'quantity' => ['required', 'integer', 'gt:0'],
'discount' => ['nullable', 'numeric', 'min:0', 'max:100'],
```

### Dates

```php
'birth_date' => ['required', 'date', 'before:today'],
'start_date' => ['required', 'date', 'after:now'],
'end_date' => ['required', 'date', 'after:start_date'],
'published_at' => ['nullable', 'date_format:Y-m-d H:i:s'],
```

### Files

```php
'avatar' => ['nullable', 'image', 'mimes:jpg,png', 'max:2048'],
'document' => ['required', 'file', 'mimes:pdf,doc,docx', 'max:10240'],
'video' => ['nullable', 'mimetypes:video/mp4', 'max:51200'], // 50MB
```

### Arrays

```php
'tags' => ['required', 'array', 'min:1', 'max:5'],
'tags.*' => ['integer', 'exists:tags,id'],
'items' => ['required', 'array'],
'items.*.name' => ['required', 'string'],
'items.*.quantity' => ['required', 'integer', 'min:1'],
```

### Enums

```php
'status' => ['required', Rule::enum({{Model}}Status::class)],
'role' => ['required', Rule::in(['admin', 'user', 'guest'])],
```

### Relationships

```php
'user_id' => ['required', 'integer', 'exists:users,id'],
'category_id' => ['nullable', 'exists:categories,id,deleted_at,NULL'], // No soft deleted
```

### Conditional Rules

```php
public function rules(): array
{
    return [
        'type' => ['required', Rule::in(['physical', 'digital'])],
        'weight' => [
            Rule::requiredIf($this->input('type') === 'physical'),
            'nullable',
            'numeric',
        ],
        'download_url' => [
            Rule::requiredIf($this->input('type') === 'digital'),
            'nullable',
            'url',
        ],
    ];
}
```

### Unique with Exceptions

```php
// Store: unique
'email' => ['required', 'email', 'unique:users'],

// Update: unique except current
public function rules(): array
{
    $user = $this->route('user');
    
    return [
        'email' => [
            'required',
            'email',
            Rule::unique('users')->ignore($user->id),
        ],
    ];
}
```

## Template - Request Test

```php
<?php

use App\Http\Requests\Store{{Model}}Request;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;

uses(RefreshDatabase::class);

describe('Store{{Model}}Request', function () {
    it('validates required fields', function () {
        $user = User::factory()->create();
        
        $response = $this->actingAs($user)
            ->postJson('/api/{{models}}', []);
        
        $response->assertUnprocessable()
            ->assertJsonValidationErrors(['name', 'status', 'price']);
    });

    it('validates string max length', function () {
        $user = User::factory()->create();
        
        $response = $this->actingAs($user)
            ->postJson('/api/{{models}}', [
                'name' => str_repeat('a', 256), // Exceeds max:255
            ]);
        
        $response->assertUnprocessable()
            ->assertJsonValidationErrors(['name']);
    });

    it('validates enum values', function () {
        $user = User::factory()->create();
        
        $response = $this->actingAs($user)
            ->postJson('/api/{{models}}', [
                'status' => 'invalid_status',
            ]);
        
        $response->assertUnprocessable()
            ->assertJsonValidationErrors(['status']);
    });

    it('validates relationship existence', function () {
        $user = User::factory()->create();
        
        $response = $this->actingAs($user)
            ->postJson('/api/{{models}}', [
                'category_id' => 999, // Non-existent
            ]);
        
        $response->assertUnprocessable()
            ->assertJsonValidationErrors(['category_id']);
    });

    it('validates image file', function () {
        $user = User::factory()->create();
        
        Storage::fake('public');
        
        $response = $this->actingAs($user)
            ->postJson('/api/{{models}}', [
                'image' => UploadedFile::fake()->create('document.pdf'), // Not an image
            ]);
        
        $response->assertUnprocessable()
            ->assertJsonValidationErrors(['image']);
    });

    it('passes with valid data', function () {
        $user = User::factory()->create();
        $category = Category::factory()->create();
        
        $response = $this->actingAs($user)
            ->postJson('/api/{{models}}', [
                'name' => 'Test {{Model}}',
                'description' => 'Test description',
                'status' => '{{Model}}Status::ACTIVE->value,
                'category_id' => $category->id,
                'price' => 99.99,
            ]);
        
        $response->assertCreated();
    });
});
```

## Checklist de Generación

- ✅ authorize() method
- ✅ rules() con todas las validaciones
- ✅ attributes() en español
- ✅ messages() personalizados
- ✅ prepareForValidation() si necesario
- ✅ Custom rules si aplican
- ✅ Conditional rules
- ✅ Tests incluidos
- ✅ PHPDoc comments
- ✅ Type hints

## Comandos Artisan

```bash
# Generar form request
php artisan make:request Store{{Model}}Request

# Generar custom rule
php artisan make:rule ValidateSlug

# Generar test
php artisan make:test Store{{Model}}RequestTest --pest
```

## Decisiones

| Campo | Validación |
|-------|------------|
| Texto corto | string, max:255 |
| Texto largo | string, max:1000 |
| Email | email:rfc,dns |
| Password | min:8, confirmed |
| Número | numeric, min, max |
| Fecha | date, after, before |
| File | file, mimes, max |
| Enum | Rule::enum() |
| Unique | Rule::unique() |
| Exists | exists:table,column |
