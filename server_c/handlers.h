#include "interface.pb.h"

int handle_set_request(SetRequest *request, Message *response);
int handle_get_request(GetRequest *request, Message *response);

int post_decode_handlers(Message *request, Message *response);
int pre_decode_handlers(Message *request, const pb_field_t *field, Message *response);
