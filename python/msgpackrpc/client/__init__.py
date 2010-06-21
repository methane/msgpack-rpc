# coding: utf-8

from msgpack import packs, Unpacker

__all__ = ['ProtocolError', 'TransportError', 'Client']

class ProtocolError(Exception):
    pass

class TransportError(Exception):
    pass

def _msgidgen():
    """Generator that generates msgid.

    NOTE: Don't use in multithread. If you want use this
    in multithreaded application, use lock.
    """
    counter = 0
    while True:
        yield counter
        counter += 1
        if counter > (1 << 30):
            counter = 0

class Client(object):
    """Simple client.
    This class is not thread safe."""
    _transport = None

    def __init__(self, transport_factory, args, kwargs):
        self._transport_factory = transport_factory
        self._transport_args = args
        self._transport_kwargs = kwargs
        self._msgidgen = _msgidgen()
        self._req_table = {}
        self._unpacker = Unpacker()

    def _get_transport(self):
        if not self._transport:
            self._transport = self._transport_factory(
                    *self._transport_args,
                    **self._transport_kwargs)
        return self._transport

    def _send_msg(self, msg):
        msg = packs(msg)
        transport = self._get_transport()
        transport.try_send(msg)

    def call_request(self, method, *args):
        """Call request synchronous.
        Return (error, result) tuple."""
        msgid = self._msgidgen.next()
        self._send_msg((0, msgid, method, args))
        return self._recv()

    def close(self):
        if self._transport:
            self._transport.try_close()
        self._transport = None

    def _recv(self):
        transport = self._get_transport()
        while True:
            data = transport.try_recv()
            self._unpacker.feed(data)
            for msg in self._unpacker:
                return self._parse_result(msg)

    def _parse_result(self, msg):
        if len(msg) != 4:
            raise ProtocolError('Invalid msgpack-rpc protocol: len(msg) = %d', len(msg))
        msgtype, msgid, msgerr, msgret = msg
        if msgtype != 1:
            raise ProtocolError('Invalid msgpack-rpc protocol: msgtype = %d', msgtype)
        return msgerr, msgret
