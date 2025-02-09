
idf_component_register(SRCS 
"server_c/device_api.c" 
"server_c/handlers.c" 
"server_c/generated/interface.pb.c"
"server_c/handlers/set_request.c"
"server_c/handlers/get_request.c"
    INCLUDE_DIRS "server_c" "server_c/generated"
    REQUIRES "main")
