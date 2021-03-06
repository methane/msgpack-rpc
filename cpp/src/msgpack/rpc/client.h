//
// msgpack::rpc::client - MessagePack-RPC for C++
//
// Copyright (C) 2010 FURUHASHI Sadayuki
//
//    Licensed under the Apache License, Version 2.0 (the "License");
//    you may not use this file except in compliance with the License.
//    You may obtain a copy of the License at
//
//        http://www.apache.org/licenses/LICENSE-2.0
//
//    Unless required by applicable law or agreed to in writing, software
//    distributed under the License is distributed on an "AS IS" BASIS,
//    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//    See the License for the specific language governing permissions and
//    limitations under the License.
//
#ifndef MSGPACK_RPC_CLIENT_H__
#define MSGPACK_RPC_CLIENT_H__

#include "types.h"
#include "session.h"
#include "loop_util.h"
#include "transport.h"
#include "address.h"
#include <mp/utilize.h>
#include <string>

namespace msgpack {
namespace rpc {


class client : public session, public loop_util<client> {
public:
	client(const std::string& host, uint16_t port, loop lo = loop());
	client(const address& addr, loop lo = loop());
	client(const builder& b, const address& addr, loop lo = loop());

	~client();

	class base;

private:
	MP_UTILIZE;

private:
	client();
};


class client::base {
public:
	base(const address& addr, loop lo = loop()) :
		instance(addr, lo) { }

	base(const std::string& host, uint16_t port, loop lo = loop()) :
		instance(host, port, lo) { }

	base(const builder& b, const address& addr, loop lo = loop()) :
		instance(b, addr, lo) { }

	rpc::client instance;

private:
	base();
};


}  // namespace rpc
}  // namespace msgpack

#endif /* msgpack/rpc/client.h */

