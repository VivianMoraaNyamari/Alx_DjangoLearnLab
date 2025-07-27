# Permissions and Groups Setup

## Custom Permissions (on `Book` model)
- `can_view`: Can view book list/details
- `can_create`: Can add a new book
- `can_edit`: Can modify existing books
- `can_delete`: Can delete books

## Groups Created
- **Viewers** → Assigned `can_view`
- **Editors** → Assigned `can_view`, `can_create`, `can_edit`
- **Admins** → Assigned all permissions

## Usage in Views
Views are protected using the `@permission_required` decorator to enforce access control. Only users with the appropriate permissions can access certain routes.