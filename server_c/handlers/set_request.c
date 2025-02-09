
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>

#include <pb_decode.h>
#include <pb_encode.h>

#include "eros.h"
#include "interface.pb.h"
#include "odin.h"
#include "odin_core.h"
#include "odin_lookup.h"
#include "odin_utils.h"
#include "srv_logging.h"

extern ODIN_parameter_group_t *device_api_odin_group;

static bool key_value_decode(pb_istream_t *stream, const pb_field_t *field,
                             void **arg) {

  Message *response = *arg;

  KeyValue key_value = KeyValue_init_zero;
  if (!pb_decode(stream, KeyValue_fields, &key_value)) {
    fprintf(stderr, "Error decoding key value\n");
    return false;
  }

  ODIN_parameter_t *parameter =
      ODIN_get_parameter_by_id(device_api_odin_group, key_value.key, 0);

  if (parameter == NULL) {
    // Set error
    response->which_content = Message_status_response_tag;
    response->content.status_response.code = StatusCodeEnum_PARAMETER_NOT_FOUND;
    return false;
  }

  // Write data to parameter
  // TODO: Acces control
  int ret =
      ODIN_parameter_write(parameter, key_value.value.bytes,
                           key_value.value.size, ODIN_ACCESS_GROUP_INTERNAL);
                           
  if (ret < ODIN_SUCCESS) {
    stream->errmsg = ODIN_error_to_string(ret);
    response->which_content = Message_status_response_tag;
    response->content.status_response.code = StatusCodeEnum_GENERAL_ERROR;
    return false;
  }

  return true;
}

int handle_set_request(SetRequest *request, Message *response) {
  request->key_values.arg = response;
  request->key_values.funcs.decode = key_value_decode;
  return StatusCodeEnum_SUCCESS;
}
