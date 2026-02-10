---
title: "From Single-File to Modular Monolith: Refactoring the Tenant Management App"
date: 2025-09-15
categories: [Learning, Architecture, Refactoring]
tags: [flask, fastapi, react, modular-monolith, refactoring, architecture, service-layer, separation-of-concerns, clean-code, api-design, frontend-backend, microservices-preparation]
content_type: "architecture-analysis"
learning_focus: ["modular-architecture", "service-layer-pattern", "clean-separation", "refactoring"]
difficulty: "intermediate"
featured: true
# Evolutionary Project Fields
project: "Tenant Management"
project_type: "evolutionary"
evolution: "Evolution 2: Modular Architecture"
evolution_number: 2
evolution_focus: "Modular Monolith"
---

Following up on my [previous post about the single-file tenant management app](/learning/full-stack-development/python/tenant-management-app-singlefile/), today I want to share the next step - refactoring it into a **modular monolith**. This was a crucial learning experience that taught me the importance of clean architecture while keeping things manageable.

> **Evolution Context**: This post is part of [Evolution 2: Modular Architecture](/projects/tenant-management/evolution-2/) in the [Tenant Management Evolutionary Project](/projects/tenant-management/). This evolution focuses on clean architecture and modular design, building upon the single-file foundation established in [Evolution 1](/projects/tenant-management/evolution-1/).

> **Requirements Context**: This modular architecture implementation is based on the detailed requirements outlined in [Landlord-Tenant Management System: Requirements and Objectives](/learning/requirements/analysis/tenant-management-requirements/). The requirements post explains the business goals and user stories that shaped both the single-file and modular implementations.

## Why Refactor?

After building the single-file version (1,655 lines!), I quickly hit some walls:
- **Maintainability**: Finding specific functionality in one massive file
- **Team Development**: Multiple developers couldn't work simultaneously  
- **Testing**: Hard to write focused unit tests
- **Code Reuse**: Business logic was tightly coupled to the web layer

The solution? **Modular Monolith Architecture** - a stepping stone toward microservices that gives you the benefits of separation without the complexity.

## The Architecture Evolution

### Before: Single File (1,655 lines)
Everything mixed together in one `app.py` file:
- HTML/CSS/JS embedded in Python
- Database models
- API routes  
- Business logic
- All in one place!

### After: Modular Monolith
Clean separation with shared database:
```
tenant-management-modular/
├── backend/                 # Flask API backend
│   ├── models.py           # Database models
│   ├── routes.py           # API endpoints
│   ├── services.py         # Business logic
│   └── config.py           # Configuration
├── fastapi_backend/        # FastAPI alternative
├── frontend/               # React SPA
└── instance/               # Shared SQLite database
```

## Key Learning Experiences

### 1. **Service Layer Pattern**
I implemented a service layer to separate business logic from API routes:

```python
class TenantService:
    @staticmethod
    def get_tenant_by_id(tenant_id):
        """Get tenant by ID with error handling."""
        tenant = Tenant.query.get(tenant_id)
        if not tenant:
            raise ValueError(f"Tenant with ID {tenant_id} not found")
        return tenant
    
    @staticmethod
    def create_tenant(data):
        """Create new tenant with validation."""
        # Business logic for tenant creation
        tenant = Tenant(**data)
        db.session.add(tenant)
        db.session.commit()
        return tenant
```

**Benefits:**
- **Reusable Logic**: Services can be used by different API endpoints
- **Testable**: Easy to unit test business logic in isolation
- **Maintainable**: Changes to business rules happen in one place

### 2. **Dual Backend Implementation**
I built both Flask and FastAPI backends to learn different approaches:

**Flask (Traditional):**
```python
@api.route('/tenants', methods=['GET'])
def get_tenants():
    """Get all tenants with optional pagination."""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        tenants = Tenant.query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'tenants': [tenant.to_dict() for tenant in tenants.items],
            'total': tenants.total
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

**FastAPI (Modern):**
```python
@app.get("/tenants", response_model=List[TenantOut])
def get_tenants(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    # Automatic validation, type hints, auto-docs
    return TenantService.get_all_tenants(db)
```

**FastAPI Advantages:**
- **Auto Documentation**: Swagger UI generated automatically
- **Type Safety**: Full type hints and validation
- **Better Performance**: Faster than Flask for API endpoints
- **Modern Python**: Async support, dependency injection

### 3. **Frontend Separation**
Moved from embedded HTML to a proper React SPA:

```javascript
// Clean component structure
function App() {
  return (
    <Router>
      <div className="App">
        <Navigation />
        <main className="main-content">
          <Routes>
            <Route path="/tenants" element={<Tenants />} />
            <Route path="/properties" element={<Properties />} />
            <Route path="/transactions" element={<Transactions />} />
          </Routes>
        </main>
        <Toaster position="top-right" />
      </div>
    </Router>
  );
}
```

**Component-Based Architecture:**
```javascript
const Tenants = () => {
  const [tenants, setTenants] = useState([]);
  const [loading, setLoading] = useState(false);
  
  const fetchTenants = useCallback(async () => {
    setLoading(true);
    try {
      const res = await axios.get(`/api/tenants?page=${page}&per_page=${perPage}`);
      setTenants(res.data.tenants || []);
    } catch (error) {
      toast.error('Failed to fetch tenants');
    } finally {
      setLoading(false);
    }
  }, [page, perPage]);
  
  // Component logic...
};
```

### 4. **Application Factory Pattern**
Implemented proper Flask application factory:

```python
def create_app(config_class=Config):
    """Application factory pattern for creating Flask app."""
    app = Flask(__name__)
    
    # Initialize configuration
    config_class.init_app(app)
    
    # Initialize extensions
    db.init_app(app)
    
    # Enable CORS for frontend
    CORS(app, origins=Config.CORS_ORIGINS)
    
    # Register blueprints
    app.register_blueprint(api)
    app.register_blueprint(swagger_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
```

### 5. **Configuration Management**
Centralized configuration with environment variables:

```python
class Config:
    """Application configuration class."""
    
    # Database configuration
    DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # CORS configuration for frontend
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
    
    @staticmethod
    def init_app(app):
        """Initialize Flask app with configuration."""
        app.config['SQLALCHEMY_DATABASE_URI'] = Config.DATABASE_URI
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS
```

## Technical Challenges and Solutions

### Challenge 1: API Communication
**Problem**: Frontend and backend running on different ports with CORS issues.

**Solution**: Proper CORS configuration and proxy setup:
```python
# Flask backend
CORS(app, origins=Config.CORS_ORIGINS)

# FastAPI backend  
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Challenge 2: State Management
**Problem**: Managing complex state across multiple React components.

**Solution**: Custom hooks and context for shared state:
```javascript
// Custom hook for API calls
const useApi = (url, options = {}) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      const response = await axios.get(url, options);
      setData(response.data);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  }, [url]);
  
  return { data, loading, error, refetch: fetchData };
};
```

### Challenge 3: Development Environment
**Problem**: Coordinating multiple services during development.

**Solution**: Development scripts and Docker Compose:
```python
# start_dev.py - Coordinated development startup
def main():
    print("Starting both backend and frontend servers...")
    backend_thread = threading.Thread(target=run_backend)
    frontend_thread = threading.Thread(target=run_frontend)
    
    backend_thread.start()
    time.sleep(2)  # Give backend time to start
    frontend_thread.start()
```

## Why Modular Monolith?

This architecture gives you the best of both worlds:

### ✅ **Benefits**
- **Clean Separation**: Each module has a single responsibility
- **Easy Testing**: Test individual components in isolation
- **Team Development**: Multiple developers can work on different modules
- **Simple Deployment**: Still one application to deploy
- **Shared Database**: No data consistency issues
- **Easy Debugging**: Everything runs in one process

### **Future Microservices Path**
The modular structure makes it easy to extract services later:
- **Tenant Service**: Extract tenant management logic
- **Property Service**: Extract property management logic  
- **Transaction Service**: Extract financial transaction logic
- **Notification Service**: Add email/SMS notifications

## Technical Implementation

### Database Sharing
Both backends use the same SQLite database with shared models.

### API Consistency
Both backends expose identical REST APIs:
```
GET /api/tenants
POST /api/tenants
PUT /api/tenants/{id}
DELETE /api/tenants/{id}
```

### Development Workflow
```bash
# Option 1: FastAPI + React
uv run uvicorn fastapi_backend.main:app --reload  # Port 8000
cd frontend && npm start                          # Port 3000

# Option 2: Flask + React  
uv run python run.py                             # Port 5000
cd frontend && npm start                          # Port 3000
```

## What I Learned About Full-Stack Development

### 1. **Separation of Concerns**
Even in a modular application, maintaining clear separation between:
- Database models
- API endpoints
- Frontend logic
- Styling

### 2. **User Experience Matters**
- Intuitive navigation with tabbed interface
- Real-time form validation
- Clear feedback for user actions
- Responsive design for different screen sizes

### 3. **Data Integrity**
- Proper foreign key relationships
- Data validation on both frontend and backend
- Audit trails with created/updated timestamps
- Consistent data serialization

### 4. **Performance Considerations**
- Efficient database queries
- Client-side pagination for large datasets
- Lazy loading of related data
- Optimized API responses

## Key Takeaways

### What I Learned
1. **Modular Monoliths are Powerful**: You get most benefits of microservices without the complexity
2. **Service Layer is Crucial**: Clean separation between API and business logic
3. **Type Safety Matters**: FastAPI's type hints catch errors early
4. **Documentation is Key**: Auto-generated docs save time and improve API adoption

### Skills Gained
- **Clean Architecture**: Proper separation of concerns
- **Service Layer Pattern**: Reusable business logic
- **API Design**: RESTful principles and consistency
- **React Development**: Component-based frontend
- **Dual Implementation**: Comparing different frameworks

## The Code

You can explore both versions:
- **Original**: [`tenant-management-app/`](https://github.com/javiator/tenant-management-applications/tree/main/tenant-management-app)
- **Modular**: [`tenant-management-modular/`](https://github.com/javiator/tenant-management-applications/tree/main/tenant-management-modular)

The modular version includes:
- Complete Flask and FastAPI backends
- React frontend with Material-UI
- Development and production setup scripts
- Comprehensive documentation
- Auto-generated API docs

## Final Thoughts

The modular monolith approach was perfect for this stage of the project. It gave me:
- **Clean Architecture**: Without over-engineering
- **Learning Experience**: Understanding service boundaries
- **Future Flexibility**: Easy path to microservices when needed
- **Maintainable Code**: Much easier to work with than the single file

If you're building applications, consider the modular monolith as a stepping stone. It's a great way to learn clean architecture principles while keeping things simple and manageable.

## Evolution Progression

This modular monolith refactoring represents a significant step in the evolutionary journey:
- **From Evolution 1**: Built upon the single-file foundation and domain understanding
- **To Evolution 2**: Introduced clean architecture and service layer patterns
- **Next Steps**: Exploring system architecture and design patterns for scalability

{% include evolution/evolution-posts.html %}

{% include evolution/post-navigation.html %}

## Conclusion

The modular monolith approach provided the perfect balance between simplicity and structure. It demonstrated the power of clean architecture principles while maintaining the operational simplicity of a single deployment unit. This foundation sets the stage for deeper architectural exploration and the eventual transition to enterprise-ready patterns.

**Next up**: I'll be exploring how to evolve this into true microservices architecture - stay tuned!
