# Django Blog - Comment System Documentation

## Overview
This document describes the complete comment system implemented in the Django Blog project.

## Features

### 1. View Comments
- **Location:** Bottom of each blog post detail page
- **Access:** Public (anyone can view)
- **Display:** Shows all comments with author, date, and content

### 2. Post Comments
- **Access:** Authenticated users only
- **Location:** Comment form at the top of comments section
- **Fields:** Content (textarea)
- **Validation:** 
  - Minimum 2 characters
  - Maximum 1000 characters

### 3. Edit Comments
- **Access:** Only the comment author
- **URL:** `/comment/<int:pk>/update/`
- **Template:** `comment_form.html`
- **Features:** Pre-filled form with existing comment

### 4. Delete Comments
- **Access:** Only the comment author
- **URL:** `/comment/<int:pk>/delete/`
- **Template:** `comment_confirm_delete.html`
- **Features:** Confirmation page before deletion

## URL Patterns

| Action | URL | Name |
|--------|-----|------|
| Create | `/post/<int:post_id>/comment/new/` | `comment-create` |
| Update | `/comment/<int:pk>/update/` | `comment-update` |
| Delete | `/comment/<int:pk>/delete/` | `comment-delete` |

## Models

### Comment Model Fields
- `post` - ForeignKey to Post
- `author` - ForeignKey to User
- `content` - TextField
- `created_at` - DateTimeField (auto_now_add=True)
- `updated_at` - DateTimeField (auto_now=True)

## Permissions Matrix

| Action | Anonymous | Authenticated | Comment Author |
|--------|-----------|---------------|----------------|
| View Comments | ✅ | ✅ | ✅ |
| Post Comment | ❌ | ✅ | ✅ |
| Edit Comment | ❌ | ❌ | ✅ |
| Delete Comment | ❌ | ❌ | ✅ |

## Implementation Details

### Views
- `CommentCreateView` - Creates new comment (LoginRequiredMixin)
- `CommentUpdateView` - Updates comment (LoginRequiredMixin + UserPassesTestMixin)
- `CommentDeleteView` - Deletes comment (LoginRequiredMixin + UserPassesTestMixin)

### Forms
- `CommentForm` - ModelForm with custom validation

### Templates
- `post_detail.html` - Displays comments and form
- `comment_form.html` - Edit comment form
- `comment_confirm_delete.html` - Delete confirmation

## Testing Instructions

### Test Posting a Comment
1. Log in to the site
2. Navigate to any blog post
3. Scroll to comments section
4. Write a comment and click "Post Comment"
5. Verify comment appears in the list

### Test Editing a Comment
1. Log in as a comment author
2. Find your comment and click "Edit"
3. Modify content and submit
4. Verify changes are saved

### Test Deleting a Comment
1. Log in as a comment author
2. Find your comment and click "Delete"
3. Confirm deletion
4. Verify comment is removed

### Test Permissions
1. Try to post a comment while logged out (should show login link)
2. Try to edit another user's comment (should not see edit button)
3. Try to delete another user's comment (should not see delete button)

## Security Features
- LoginRequiredMixin for creating comments
- UserPassesTestMixin for author-only actions
- CSRF protection on all forms
- Input validation and sanitization
- SQL injection protection via Django ORM

## Dependencies
- Django 6.0.1
- Bootstrap 4.5 (for styling)
- SQLite (database)
