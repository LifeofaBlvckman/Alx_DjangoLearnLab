cat > DEPLOYMENT.md << 'EOF'
# Social Media API - Deployment Documentation

## Live URL
**https://social-media-api-b93m.onrender.com**

## Deployment Platform
- **Hosting Service:** Render (https://render.com)
- **Web Server:** Gunicorn
- **Database:** PostgreSQL (via Render)
- **Static Files:** WhiteNoise

## Environment Configuration
The following environment variables are configured:
- `DJANGO_SECRET_KEY`: Production secret key
- `DEBUG`: False
- `ALLOWED_HOSTS`: social-media-api-b93m.onrender.com,localhost,127.0.0.1
- `DATABASE_URL`: PostgreSQL connection string

## Deployment Process
1. Code pushed to GitHub repository
2. Render automatically detects changes
3. Build process installs dependencies
4. Migrations run automatically
5. Static files collected
6. App deployed with Gunicorn

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Create new account
- `POST /api/auth/login/` - Login and get token
- `POST /api/auth/logout/` - Logout
- `GET /api/auth/profile/` - View profile
- `GET /api/auth/profile/<id>/` - View other user's profile

### Posts
- `GET /api/posts/` - List all posts
- `POST /api/posts/` - Create new post
- `GET /api/posts/<id>/` - View specific post
- `PUT /api/posts/<id>/` - Update post
- `DELETE /api/posts/<id>/` - Delete post
- `POST /api/posts/<id>/like/` - Like a post
- `POST /api/posts/<id>/unlike/` - Unlike a post

### Comments
- `GET /api/comments/` - List comments
- `POST /api/comments/` - Create comment
- `GET /api/comments/<id>/` - View comment
- `PUT /api/comments/<id>/` - Update comment
- `DELETE /api/comments/<id>/` - Delete comment

### Feed & Follows
- `GET /api/feed/` - Get posts from followed users
- `POST /api/auth/follow/<user_id>/` - Follow user
- `POST /api/auth/unfollow/<user_id>/` - Unfollow user
- `GET /api/auth/followers/<user_id>/` - Get followers
- `GET /api/auth/following/<user_id>/` - Get following

### Notifications
- `GET /api/notifications/` - Get notifications
- `POST /api/notifications/<id>/read/` - Mark as read
- `GET /api/notifications/unread-count/` - Get unread count

## Testing the Live API

### Using curl
```bash
# Register a user
curl -X POST https://social-media-api-b93m.onrender.com/api/auth/register/ \\
  -H "Content-Type: application/json" \\
  -d '{"username":"testuser","email":"test@example.com","password":"test123","password2":"test123"}'

# Login
curl -X POST https://social-media-api-b93m.onrender.com/api/auth/login/ \\
  -H "Content-Type: application/json" \\
  -d '{"username":"testuser","password":"test123"}'

# Create a post (with token)
curl -X POST https://social-media-api-b93m.onrender.com/api/posts/ \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Token YOUR_TOKEN_HERE" \\
  -d '{"title":"My First Post","content":"Hello from production!"}'
