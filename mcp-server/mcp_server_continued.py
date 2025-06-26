            method, endpoint = action_map[action]
            return await api_request(method, endpoint, args if method == "POST" else None, session_id)
        
        # Handle message updates
        if action == "update_message":
            message_id = args.pop("message_id")
            return await api_request("POST", f"/api/v1/chats/{chat_id}/messages/{message_id}", args, session_id)
    
    # Handle other chat operations
    if tool_name == "chats_get_shared":
        share_id = args.get("share_id")
        return await api_request("GET", f"/api/v1/chats/share/{share_id}", None, session_id)
    elif tool_name == "chats_get_folder":
        folder_id = args.get("folder_id")
        return await api_request("GET", f"/api/v1/chats/folder/{folder_id}", None, session_id)
    elif tool_name == "chats_get_by_user":
        user_id = args.get("user_id")
        return await api_request("GET", f"/api/v1/chats/list/user/{user_id}", None, session_id)
    
    return {"error": f"Unknown chat tool: {tool_name}"}

async def handle_file_tools(tool_name: str, args: Dict, session_id: str) -> Dict:
    """Handle file tools"""
    if tool_name == "files_list":
        return await api_request("GET", "/api/v1/files/", None, session_id)
    elif tool_name == "files_upload":
        return await api_request("POST", "/api/v1/files/", args, session_id)
    elif tool_name == "files_batch_upload":
        return await api_request("POST", "/api/v1/files/batch", args, session_id)
    elif tool_name == "files_search":
        return await api_request("GET", f"/api/v1/files/search?query={args.get('query', '')}", None, session_id)
    
    # File-specific operations
    if tool_name.startswith("files_") and "file_id" in args:
        file_id = args.pop("file_id")
        action = tool_name.replace("files_", "")
        
        action_map = {
            "get": ("GET", f"/api/v1/files/{file_id}"),
            "delete": ("DELETE", f"/api/v1/files/{file_id}"),
            "update": ("POST", f"/api/v1/files/{file_id}"),
            "get_content": ("GET", f"/api/v1/files/{file_id}/content"),
            "download": ("GET", f"/api/v1/files/{file_id}/download"),
            "get_metadata": ("GET", f"/api/v1/files/{file_id}/metadata"),
        }
        
        if action in action_map:
            method, endpoint = action_map[action]
            return await api_request(method, endpoint, args if method == "POST" else None, session_id)
    
    return {"error": f"Unknown file tool: {tool_name}"}

async def handle_rag_tools(tool_name: str, args: Dict, session_id: str) -> Dict:
    """Handle RAG/Knowledge tools"""
    # Knowledge collection tools
    if tool_name == "knowledge_list":
        return await api_request("GET", "/api/v1/knowledge/", None, session_id)
    elif tool_name == "knowledge_create":
        return await api_request("POST", "/api/v1/knowledge/create", args, session_id)
    
    # Knowledge-specific operations
    if tool_name.startswith("knowledge_") and "knowledge_id" in args:
        knowledge_id = args.pop("knowledge_id")
        action = tool_name.replace("knowledge_", "")
        
        if action == "get":
            return await api_request("GET", f"/api/v1/knowledge/{knowledge_id}", None, session_id)
        elif action == "update":
            return await api_request("POST", f"/api/v1/knowledge/{knowledge_id}/update", args, session_id)
        elif action == "delete":
            return await api_request("DELETE", f"/api/v1/knowledge/{knowledge_id}", None, session_id)
        elif action == "add_file":
            return await api_request("POST", f"/api/v1/knowledge/{knowledge_id}/file/add", args, session_id)
        elif action == "remove_file":
            return await api_request("POST", f"/api/v1/knowledge/{knowledge_id}/file/remove", args, session_id)
    
    # RAG system tools
    rag_map = {
        "rag_status": ("/api/v1/retrieval/", "GET"),
        "rag_config_get": ("/api/v1/retrieval/config", "GET"),
        "rag_config_update": ("/api/v1/retrieval/config", "POST"),
        "rag_process_text": ("/api/v1/retrieval/process/text", "POST"),
        "rag_process_file": ("/api/v1/retrieval/process/file", "POST"),
        "rag_process_web": ("/api/v1/retrieval/process/web", "POST"),
        "rag_process_youtube": ("/api/v1/retrieval/process/youtube", "POST"),
        "rag_query_doc": ("/api/v1/retrieval/query/doc", "POST"),
        "rag_query_collection": ("/api/v1/retrieval/query/collection", "POST"),
        "rag_delete": ("/api/v1/retrieval/delete", "POST"),
        "rag_reset_db": ("/api/v1/retrieval/reset/db", "POST"),
        "rag_reset_uploads": ("/api/v1/retrieval/reset/uploads", "POST"),
        "rag_get_embeddings": ("/api/v1/retrieval/ef", "POST"),
    }
    
    if tool_name in rag_map:
        endpoint, method = rag_map[tool_name]
        return await api_request(method, endpoint, args if method == "POST" else None, session_id)
    
    return {"error": f"Unknown RAG tool: {tool_name}"}

async def handle_prompt_tools(tool_name: str, args: Dict, session_id: str) -> Dict:
    """Handle prompt tools"""
    if tool_name == "prompts_list":
        return await api_request("GET", "/api/v1/prompts/", None, session_id)
    elif tool_name == "prompts_create":
        return await api_request("POST", "/api/v1/prompts/create", args, session_id)
    elif tool_name == "prompts_search":
        return await api_request("GET", f"/api/v1/prompts/search?query={args.get('query', '')}", None, session_id)
    elif tool_name == "prompts_get_by_command":
        return await api_request("GET", f"/api/v1/prompts/command/{args.get('command', '')}", None, session_id)
    elif tool_name == "prompts_get_categories":
        return await api_request("GET", "/api/v1/prompts/categories", None, session_id)
    elif tool_name == "prompts_get_tags":
        return await api_request("GET", "/api/v1/prompts/tags", None, session_id)
    
    # Prompt-specific operations
    if tool_name.startswith("prompts_") and "prompt_id" in args:
        prompt_id = args.pop("prompt_id")
        action = tool_name.replace("prompts_", "")
        
        action_map = {
            "get": ("GET", f"/api/v1/prompts/{prompt_id}"),
            "update": ("POST", f"/api/v1/prompts/{prompt_id}/update"),
            "delete": ("DELETE", f"/api/v1/prompts/{prompt_id}"),
            "execute": ("POST", f"/api/v1/prompts/{prompt_id}/execute"),
        }
        
        if action in action_map:
            method, endpoint = action_map[action]
            return await api_request(method, endpoint, args if method == "POST" else None, session_id)
    
    return {"error": f"Unknown prompt tool: {tool_name}"}

async def handle_function_tools(tool_name: str, args: Dict, session_id: str) -> Dict:
    """Handle function tools"""
    if tool_name == "functions_list":
        return await api_request("GET", "/api/v1/functions/", None, session_id)
    elif tool_name == "functions_create":
        return await api_request("POST", "/api/v1/functions/create", args, session_id)
    
    # Function-specific operations
    if tool_name.startswith("functions_") and "function_id" in args:
        function_id = args.pop("function_id")
        action = tool_name.replace("functions_", "")
        
        action_map = {
            "get": ("GET", f"/api/v1/functions/{function_id}"),
            "update": ("POST", f"/api/v1/functions/{function_id}/update"),
            "delete": ("DELETE", f"/api/v1/functions/{function_id}"),
            "update_valves": ("POST", f"/api/v1/functions/{function_id}/valves/update"),
            "get_valves": ("GET", f"/api/v1/functions/{function_id}/valves"),
            "execute": ("POST", f"/api/v1/functions/{function_id}/execute"),
            "test": ("POST", f"/api/v1/functions/{function_id}/test"),
            "get_schema": ("GET", f"/api/v1/functions/{function_id}/schema"),
        }
        
        if action in action_map:
            method, endpoint = action_map[action]
            return await api_request(method, endpoint, args if method == "POST" else None, session_id)
    
    return {"error": f"Unknown function tool: {tool_name}"}

async def handle_memory_tools(tool_name: str, args: Dict, session_id: str) -> Dict:
    """Handle memory tools"""
    if tool_name == "memories_list":
        return await api_request("GET", "/api/v1/memories/", None, session_id)
    elif tool_name == "memories_add":
        return await api_request("POST", "/api/v1/memories/add", args, session_id)
    elif tool_name == "memories_reset":
        return await api_request("POST", "/api/v1/memories/reset", None, session_id)
    elif tool_name == "memories_search":
        return await api_request("GET", f"/api/v1/memories/search?query={args.get('query', '')}", None, session_id)
    elif tool_name == "memories_get_context":
        return await api_request("POST", "/api/v1/memories/context", args, session_id)
    
    # Memory-specific operations
    if tool_name.startswith("memories_") and "memory_id" in args:
        memory_id = args.pop("memory_id")
        action = tool_name.replace("memories_", "")
        
        action_map = {
            "get": ("GET", f"/api/v1/memories/{memory_id}"),
            "update": ("POST", f"/api/v1/memories/{memory_id}/update"),
            "delete": ("DELETE", f"/api/v1/memories/{memory_id}"),
        }
        
        if action in action_map:
            method, endpoint = action_map[action]
            return await api_request(method, endpoint, args if method == "POST" else None, session_id)
    
    return {"error": f"Unknown memory tool: {tool_name}"}

async def handle_folder_tools(tool_name: str, args: Dict, session_id: str) -> Dict:
    """Handle folder tools"""
    if tool_name == "folders_list":
        return await api_request("GET", "/api/v1/folders/", None, session_id)
    elif tool_name == "folders_create":
        return await api_request("POST", "/api/v1/folders/create", args, session_id)
    
    # Folder-specific operations
    if tool_name.startswith("folders_") and "folder_id" in args:
        folder_id = args.pop("folder_id")
        action = tool_name.replace("folders_", "")
        
        action_map = {
            "get": ("GET", f"/api/v1/folders/{folder_id}"),
            "update": ("POST", f"/api/v1/folders/{folder_id}/update"),
            "delete": ("DELETE", f"/api/v1/folders/{folder_id}"),
            "get_contents": ("GET", f"/api/v1/folders/{folder_id}/contents"),
            "get_path": ("GET", f"/api/v1/folders/{folder_id}/path"),
        }
        
        if action in action_map:
            method, endpoint = action_map[action]
            return await api_request(method, endpoint, args if method == "POST" else None, session_id)
        
        if action == "move_item":
            return await api_request("POST", f"/api/v1/folders/{folder_id}/move", args, session_id)
    
    return {"error": f"Unknown folder tool: {tool_name}"}

async def handle_config_tools(tool_name: str, args: Dict, session_id: str) -> Dict:
    """Handle configuration tools"""
    config_map = {
        "config_export": ("/api/v1/configs/export", "GET"),
        "config_import": ("/api/v1/configs/import", "POST"),
        "config_models_get": ("/api/v1/configs/models", "GET"),
        "config_models_update": ("/api/v1/configs/models", "POST"),
        "config_tool_servers_get": ("/api/v1/configs/tool_servers", "GET"),
        "config_tool_servers_update": ("/api/v1/configs/tool_servers", "POST"),
        "config_tool_servers_verify": ("/api/v1/configs/tool_servers/verify", "POST"),
        "config_suggestions_update": ("/api/v1/configs/suggestions", "POST"),
        "config_banners_get": ("/api/v1/configs/banners", "GET"),
        "config_banners_update": ("/api/v1/configs/banners", "POST"),
        "config_code_execution_get": ("/api/v1/configs/code_execution", "GET"),
        "config_code_execution_update": ("/api/v1/configs/code_execution", "POST"),
        "config_direct_connections_get": ("/api/v1/configs/direct_connections", "GET"),
        "config_direct_connections_update": ("/api/v1/configs/direct_connections", "POST"),
        "config_reset": ("/api/v1/configs/reset", "POST"),
    }
    
    if tool_name in config_map:
        endpoint, method = config_map[tool_name]
        return await api_request(method, endpoint, args if method == "POST" else None, session_id)
    
    return {"error": f"Unknown config tool: {tool_name}"}

async def handle_task_tools(tool_name: str, args: Dict, session_id: str) -> Dict:
    """Handle task tools"""
    task_map = {
        "tasks_config_get": ("/api/v1/tasks/config", "GET"),
        "tasks_config_update": ("/api/v1/tasks/config/update", "POST"),
        "tasks_generate_title": ("/api/v1/tasks/title/completions", "POST"),
        "tasks_generate_followup": ("/api/v1/tasks/follow_up/completions", "POST"),
        "tasks_generate_tags": ("/api/v1/tasks/tags/completions", "POST"),
        "tasks_generate_image_prompt": ("/api/v1/tasks/image_prompt/completions", "POST"),
        "tasks_generate_queries": ("/api/v1/tasks/queries/completions", "POST"),
        "tasks_generate_auto": ("/api/v1/tasks/auto/completions", "POST"),
        "tasks_generate_emoji": ("/api/v1/tasks/emoji/completions", "POST"),
        "tasks_generate_moa": ("/api/v1/tasks/moa/completions", "POST"),
        "tasks_generate_summary": ("/api/v1/tasks/summary/completions", "POST"),
        "tasks_generate_keywords": ("/api/v1/tasks/keywords/completions", "POST"),
        "tasks_generate_outline": ("/api/v1/tasks/outline/completions", "POST"),
        "tasks_generate_ideas": ("/api/v1/tasks/ideas/completions", "POST"),
        "tasks_execute": ("/api/v1/tasks/execute", "POST"),
    }
    
    if tool_name in task_map:
        endpoint, method = task_map[tool_name]
        return await api_request(method, endpoint, args if method == "POST" else None, session_id)
    
    return {"error": f"Unknown task tool: {tool_name}"}

async def handle_media_tools(tool_name: str, args: Dict, session_id: str) -> Dict:
    """Handle image and audio tools"""
    media_map = {
        "images_config_get": ("/api/v1/images/config", "GET"),
        "images_config_update": ("/api/v1/images/config/update", "POST"),
        "images_models_list": ("/api/v1/images/models", "GET"),
        "images_generate": ("/api/v1/images/generations", "POST"),
        "images_edit": ("/api/v1/images/edit", "POST"),
        "audio_config_get": ("/api/v1/audio/config", "GET"),
        "audio_config_update": ("/api/v1/audio/config/update", "POST"),
        "audio_speech": ("/api/v1/audio/speech", "POST"),
        "audio_transcribe": ("/api/v1/audio/transcriptions", "POST"),
        "audio_models_list": ("/api/v1/audio/models", "GET"),
    }
    
    if tool_name in media_map:
        endpoint, method = media_map[tool_name]
        return await api_request(method, endpoint, args if method == "POST" else None, session_id)
    
    return {"error": f"Unknown media tool: {tool_name}"}

async def handle_pipeline_tools(tool_name: str, args: Dict, session_id: str) -> Dict:
    """Handle pipeline tools"""
    if tool_name == "pipelines_list":
        return await api_request("GET", "/api/v1/pipelines/list", None, session_id)
    elif tool_name == "pipelines_upload":
        return await api_request("POST", "/api/v1/pipelines/upload", args, session_id)
    elif tool_name == "pipelines_add":
        return await api_request("POST", "/api/v1/pipelines/add", args, session_id)
    
    # Pipeline-specific operations
    if tool_name.startswith("pipelines_") and "pipeline_id" in args:
        pipeline_id = args.pop("pipeline_id")
        action = tool_name.replace("pipelines_", "")
        
        action_map = {
            "delete": ("DELETE", f"/api/v1/pipelines/delete"),
            "get_valves": ("GET", f"/api/v1/pipelines/{pipeline_id}/valves"),
            "update_valves": ("POST", f"/api/v1/pipelines/{pipeline_id}/valves/update"),
            "execute": ("POST", f"/api/v1/pipelines/{pipeline_id}/execute"),
            "get_schema": ("GET", f"/api/v1/pipelines/{pipeline_id}/schema"),
            "test": ("POST", f"/api/v1/pipelines/{pipeline_id}/test"),
            "get_logs": ("GET", f"/api/v1/pipelines/{pipeline_id}/logs"),
        }
        
        if action in action_map:
            method, endpoint = action_map[action]
            # For delete, pipeline_id goes in body
            if action == "delete":
                args["pipeline_id"] = pipeline_id
            return await api_request(method, endpoint, args if method in ["POST", "DELETE"] else None, session_id)
    
    return {"error": f"Unknown pipeline tool: {tool_name}"}

async def handle_compound_tools(tool_name: str, args: Dict, session_id: str) -> Dict:
    """Handle compound operations - Master Builder Tools"""
    if tool_name == "create_workspace":
        return await create_complete_workspace(args, session_id)
    elif tool_name == "create_instabids_mobile_workspace":
        return await create_instabids_mobile_workspace(session_id)
    elif tool_name == "create_instabridge_api_workspace":
        return await create_instabridge_api_workspace(session_id)
    elif tool_name == "create_general_dev_workspace":
        project_name = args.get("project_name", "New Project")
        return await create_general_dev_workspace(project_name, session_id)
    elif tool_name == "setup_complete_system":
        return await setup_complete_instabids_system(session_id)
    
    return {"error": f"Unknown compound tool: {tool_name}"}

# Compound operation implementations

async def create_complete_workspace(args: Dict, session_id: str) -> Dict:
    """Create a complete AI workspace"""
    name = args.get("name", "New Workspace")
    model = args.get("model", "gpt-4")
    system_prompt = args.get("system_prompt", "You are a helpful AI assistant.")
    
    chat_data = {
        "chat": {
            "title": name,
            "messages": [{"role": "system", "content": system_prompt}],
            "models": [model],
            "tags": ["workspace", "created-by-mcp"]
        }
    }
    
    result = await api_request("POST", "/api/v1/chats/new", chat_data, session_id)
    
    if result["success"]:
        return {
            "status": "success",
            "workspace_id": result["data"].get("id"),
            "message": f"Workspace '{name}' created successfully!",
            "details": {
                "name": name,
                "model": model,
                "prompt_preview": system_prompt[:100] + "..."
            }
        }
    else:
        return {
            "status": "error",
            "message": "Failed to create workspace",
            "error": result["data"]
        }

async def create_instabids_mobile_workspace(session_id: str) -> Dict:
    """Create InstaBids mobile development workspace"""
    system_prompt = """You are an expert React Native developer for InstaBids mobile app.

🎯 Your Role:
- React Native/Expo development specialist
- Focus on InstaBids mobile app patterns
- Use NativeWind for styling (Tailwind for React Native)
- Implement Zustand for state management

🏗️ Tech Stack:
- React Native with Expo
- TypeScript
- NativeWind (Tailwind CSS for React Native)
- Zustand for state management
- React Navigation

🎨 InstaBids Brand Colors:
- Primary: #1E40AF (blue)
- Secondary: #F59E0B (orange)
- Success: #10B981 (green)
- Error: #EF4444 (red)

📱 Development Focus:
- Component-driven development
- Clean, reusable UI components
- Mobile-first responsive design
- Performance optimization
- Following InstaBids patterns"""
    
    return await create_complete_workspace({
        "name": "InstaBids Mobile Developer",
        "model": "gpt-4",
        "system_prompt": system_prompt
    }, session_id)

async def create_instabridge_api_workspace(session_id: str) -> Dict:
    """Create InstaBridge API development workspace"""
    system_prompt = """You are a backend API expert for InstaBridge integration platform.

🎯 Your Role:
- Node.js/TypeScript API development
- InstaBridge integration platform specialist
- Security and authentication expert
- Third-party service integrations

🏗️ Tech Stack:
- Node.js with TypeScript
- Express.js framework
- PostgreSQL (Supabase)
- JWT authentication
- RESTful API design

🔧 Key Responsibilities:
- API endpoint design and implementation
- Database schema design
- Authentication and authorization
- Third-party API integrations
- Error handling and logging
- API documentation

🛡️ Security Focus:
- Input validation and sanitization
- Proper authentication flows
- Rate limiting and CORS
- Environment variable management"""
    
    return await create_complete_workspace({
        "name": "InstaBridge API Developer",
        "model": "gpt-4",
        "system_prompt": system_prompt
    }, session_id)

async def create_general_dev_workspace(project_name: str, session_id: str) -> Dict:
    """Create general development workspace"""
    system_prompt = f"""You are a full-stack developer working on {project_name}.

🎯 Your Role:
- Full-stack development expert
- Follow InstaBids coding standards
- Modern development practices
- Clean, maintainable code focus

🏗️ InstaBids Tech Standards:
- Frontend: React Native (mobile) or Next.js (web)
- Backend: Node.js with TypeScript
- Database: PostgreSQL (Supabase)
- Styling: NativeWind or Tailwind CSS
- State: Zustand

🎨 Brand Colors:
- Primary: #1E40AF
- Secondary: #F59E0B
- Success: #10B981
- Error: #EF4444

📋 Development Principles:
- Component-driven development
- Type safety with TypeScript
- Clean code and documentation
- Performance optimization
- Mobile-first design

Project: {project_name}"""
    
    return await create_complete_workspace({
        "name": f"{project_name} Developer",
        "model": "gpt-4",
        "system_prompt": system_prompt
    }, session_id)

async def setup_complete_instabids_system(session_id: str) -> Dict:
    """Setup the complete InstaBids AI system"""
    results = []
    
    try:
        # Create all workspaces
        mobile_result = await create_instabids_mobile_workspace(session_id)
        results.append("✅ InstaBids Mobile workspace" if mobile_result.get("status") == "success" else "❌ Mobile workspace failed")
        
        api_result = await create_instabridge_api_workspace(session_id)
        results.append("✅ InstaBridge API workspace" if api_result.get("status") == "success" else "❌ API workspace failed")
        
        general_result = await create_general_dev_workspace("InstaBids Core", session_id)
        results.append("✅ General development workspace" if general_result.get("status") == "success" else "❌ General workspace failed")
        
        # Add company knowledge
        knowledge_data = {
            "name": "InstaBids Company Guidelines",
            "content": """InstaBids Development Guidelines:

BRAND COLORS:
- Primary: #1E40AF (blue)
- Secondary: #F59E0B (orange)
- Success: #10B981 (green)
- Error: #EF4444 (red)

TECH STACK:
- Mobile: React Native + Expo + NativeWind + Zustand
- Backend: Node.js + TypeScript + Express + Supabase
- Database: PostgreSQL (Supabase)
- Authentication: JWT tokens

DEVELOPMENT PRINCIPLES:
- Component-driven development
- Type safety with TypeScript
- Clean code and documentation
- Mobile-first responsive design
- Performance optimization

PROJECT STRUCTURE:
- instabids/instabids (main mobile app)
- instabids/instabridge (integration platform)
- instabids/backend-api (core API services)""",
            "collection_name": "instabids-company"
        }
        
        knowledge_result = await api_request("POST", "/api/v1/retrieval/process/text", knowledge_data, session_id)
        results.append("✅ Company knowledge base" if knowledge_result["success"] else "❌ Knowledge base failed")
        
    except Exception as e:
        results.append(f"⚠️ Error: {str(e)}")
    
    return {
        "status": "complete",
        "results": results,
        "summary": f"""🚀 InstaBids AI System Setup Complete!

{chr(10).join(results)}

🎯 Available Workspaces:
1. InstaBids Mobile Developer (React Native/Expo specialist)
2. InstaBridge API Developer (Node.js/TypeScript expert)
3. InstaBids Core Developer (Full-stack generalist)

💡 Usage Instructions:
- Start any chat and say "Switch to [Workspace Name]"
- Each workspace has specialized knowledge and context
- All workspaces know InstaBids brand guidelines and tech standards

Your AI development environment is ready! 🎉"""
    }

# Server lifecycle

async def cleanup():
    """Cleanup on shutdown"""
    logger.info("Cleaning up resources...")
    
    # Close all HTTP sessions
    for session_id, session in sessions.items():
        await session.close()
    
    # Close Redis connection
    await session_manager.close()
    
    logger.info("Cleanup complete")

async def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Check Open WebUI connection
        result = await api_request("GET", "/health")
        openwebui_status = "healthy" if result["success"] else "unhealthy"
        
        # Check Redis connection
        redis_status = await session_manager.health_check()
        
        return {
            "status": "healthy" if openwebui_status == "healthy" and redis_status else "unhealthy",
            "components": {
                "openwebui": openwebui_status,
                "redis": "healthy" if redis_status else "unhealthy",
                "mcp_server": "healthy"
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }

async def main():
    """Run the MCP server"""
    logger.info(f"Starting Open WebUI MCP Server on port {PORT}")
    logger.info(f"Open WebUI URL: {OPENWEBUI_URL}")
    logger.info(f"Redis URL: {REDIS_URL}")
    
    # Initialize session manager
    await session_manager.initialize()
    
    # Run health check
    health = await health_check()
    logger.info(f"Health check: {health}")
    
    # Run MCP server
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        try:
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="openwebui-cloud",
                    server_version="2.0.0",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )
        finally:
            await cleanup()

if __name__ == "__main__":
    # Configure logging
    logger.add("mcp_server.log", rotation="10 MB", retention="7 days")
    
    # Run the server
    asyncio.run(main())