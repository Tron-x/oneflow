from __future__ import absolute_import

import oneflow.python.framework.compile_context as compile_context
import oneflow.python.framework.remote_blob as remote_blob_util
import oneflow.python.framework.id_util as id_util
import oneflow.core.operator.op_conf_pb2 as op_conf_util
import oneflow.core.register.logical_blob_id_pb2 as logical_blob_id_util

from oneflow.python.oneflow_export import oneflow_export


@oneflow_export("math.add")
def add(x, y, name=None):
    if isinstance(x, (int, float)):
        return scalar_add(y, x, name)
    elif isinstance(y, (int, float)):
        return scalar_add(x, y, name)
    elif x.static_shape == y.static_shape and x.batch_axis == y.batch_axis:
        return element_wise_add(x, y, name)
    else:
        return broadcast_add(x, y, name)


@oneflow_export("math.subtract")
def subtract(x, y, name=None):
    if isinstance(x, (int, float)):
        return scalar_add(-1 * y, x, name)
    elif isinstance(y, (int, float)):
        return scalar_add(x, -1 * y, name)
    elif x.static_shape == y.static_shape:
        # TODO: add element-wise op
        return broadcast_sub(x, y, name)
    else:
        return broadcast_sub(x, y, name)


@oneflow_export("math.multiply")
def multiply(x, y, name=None):
    if isinstance(x, (int, float)):
        return scalar_mul(y, x, name)
    elif isinstance(y, (int, float)):
        return scalar_mul(x, y, name)
    elif x.static_shape == y.static_shape:
        # TODO: add element-wise op
        return broadcast_mul(x, y, name)
    else:
        return broadcast_mul(x, y, name)


@oneflow_export("math.divide")
def divide(x, y, name=None):
    if isinstance(x, (int, float)):
        raise NotImplementedError
    elif isinstance(y, (int, float)):
        raise NotImplementedError
    elif x.static_shape == y.static_shape:
        # TODO: add element-wise op
        return broadcast_div(x, y, name)
    else:
        return broadcast_div(x, y, name)


def scalar_add(x, operand, name=None):
    op_conf = op_conf_util.OperatorConf()
    setattr(
        op_conf, "name", name if name is not None else id_util.UniqueStr("ScalarAdd_")
    )
    setattr(op_conf.scalar_add_conf, "in", x.logical_blob_name)
    if isinstance(operand, int):
        op_conf.scalar_add_conf.int_operand = operand
    elif isinstance(operand, float):
        op_conf.scalar_add_conf.float_operand = operand
    op_conf.scalar_add_conf.out = "out"
    compile_context.CurJobAddOp(op_conf)
    lbi = logical_blob_id_util.LogicalBlobId()
    lbi.op_name = op_conf.name
    lbi.blob_name = "out"
    return remote_blob_util.RemoteBlob(lbi)


def element_wise_add(x, y, name=None):
    op_conf = op_conf_util.OperatorConf()
    setattr(
        op_conf,
        "name",
        name if name is not None else id_util.UniqueStr("ElementWiseAdd_"),
    )
    getattr(op_conf.add_conf, "in").append(x.logical_blob_name)
    getattr(op_conf.add_conf, "in").append(y.logical_blob_name)
    op_conf.add_conf.out = "out"
    compile_context.CurJobAddOp(op_conf)
    lbi = logical_blob_id_util.LogicalBlobId()
    lbi.op_name = op_conf.name
    lbi.blob_name = "out"
    return remote_blob_util.RemoteBlob(lbi)


def broadcast_add(x, y, name=None):
    op_conf = op_conf_util.OperatorConf()
    setattr(
        op_conf,
        "name",
        name if name is not None else id_util.UniqueStr("BroadcastAdd_"),
    )
    op_conf.broadcast_add_conf.a = x.logical_blob_name
    op_conf.broadcast_add_conf.b = y.logical_blob_name
    op_conf.broadcast_add_conf.out = "out"
    compile_context.CurJobAddOp(op_conf)
    lbi = logical_blob_id_util.LogicalBlobId()
    lbi.op_name = op_conf.name
    lbi.blob_name = "out"
    return remote_blob_util.RemoteBlob(lbi)


def broadcast_sub(x, y, name=None):
    op_conf = op_conf_util.OperatorConf()
    setattr(
        op_conf,
        "name",
        name if name is not None else id_util.UniqueStr("BroadcastSub_"),
    )
    op_conf.broadcast_sub_conf.a = x.logical_blob_name
    op_conf.broadcast_sub_conf.b = y.logical_blob_name
    op_conf.broadcast_sub_conf.out = "out"
    compile_context.CurJobAddOp(op_conf)
    lbi = logical_blob_id_util.LogicalBlobId()
    lbi.op_name = op_conf.name
    lbi.blob_name = "out"
    return remote_blob_util.RemoteBlob(lbi)


def broadcast_mul(x, y, name=None):
    op_conf = op_conf_util.OperatorConf()
    setattr(
        op_conf,
        "name",
        name if name is not None else id_util.UniqueStr("BroadcastMul_"),
    )
    op_conf.broadcast_mul_conf.a = x.logical_blob_name
    op_conf.broadcast_mul_conf.b = y.logical_blob_name
    op_conf.broadcast_mul_conf.out = "out"
    compile_context.CurJobAddOp(op_conf)
    lbi = logical_blob_id_util.LogicalBlobId()
    lbi.op_name = op_conf.name
    lbi.blob_name = "out"
    return remote_blob_util.RemoteBlob(lbi)


def scalar_mul(x, operand, name=None):
    op_conf = op_conf_util.OperatorConf()
    setattr(
        op_conf, "name", name if name is not None else id_util.UniqueStr("ScalarMul_")
    )
    setattr(op_conf.scalar_mul_conf, "in", x.logical_blob_name)
    if isinstance(operand, int):
        op_conf.scalar_mul_conf.int_operand = operand
    elif isinstance(operand, float):
        op_conf.scalar_mul_conf.float_operand = operand
    op_conf.scalar_mul_conf.out = "out"
    compile_context.CurJobAddOp(op_conf)
    lbi = logical_blob_id_util.LogicalBlobId()
    lbi.op_name = op_conf.name
    lbi.blob_name = "out"
    return remote_blob_util.RemoteBlob(lbi)


def broadcast_div(x, y, name=None):
    op_conf = op_conf_util.OperatorConf()
    setattr(
        op_conf,
        "name",
        name if name is not None else id_util.UniqueStr("BroadcastDiv_"),
    )
    op_conf.broadcast_div_conf.a = x.logical_blob_name
    op_conf.broadcast_div_conf.b = y.logical_blob_name
    op_conf.broadcast_div_conf.out = "out"
    compile_context.CurJobAddOp(op_conf)
    lbi = logical_blob_id_util.LogicalBlobId()
    lbi.op_name = op_conf.name
    lbi.blob_name = "out"
    return remote_blob_util.RemoteBlob(lbi)


@oneflow_export("math.tanh")
def tanh(x, name=None):
    op_conf = op_conf_util.OperatorConf()
    setattr(op_conf, "name", name if name is not None else id_util.UniqueStr("TanH_"))
    setattr(op_conf.tanh_conf, "in", x.logical_blob_name)
    setattr(op_conf.tanh_conf, "out", "out")
    compile_context.CurJobAddOp(op_conf)
    lbi = logical_blob_id_util.LogicalBlobId()
    lbi.op_name = op_conf.name
    lbi.blob_name = "out"
    return remote_blob_util.RemoteBlob(lbi)


@oneflow_export("math.gelu")
def gelu(x, name=None):
    op_conf = op_conf_util.OperatorConf()
    setattr(op_conf, "name", name if name is not None else id_util.UniqueStr("Gelu_"))
    setattr(op_conf.gelu_conf, "in", x.logical_blob_name)
    setattr(op_conf.gelu_conf, "out", "out")
    compile_context.CurJobAddOp(op_conf)
    lbi = logical_blob_id_util.LogicalBlobId()
    lbi.op_name = op_conf.name
    lbi.blob_name = "out"
    return remote_blob_util.RemoteBlob(lbi)


@oneflow_export("math.relu")
def relu(x, name=None):
    op_conf = op_conf_util.OperatorConf()
    setattr(op_conf, "name", name if name is not None else id_util.UniqueStr("Relu_"))
    setattr(op_conf.relu_conf, "in", x.logical_blob_name)
    setattr(op_conf.relu_conf, "out", "out")
    compile_context.CurJobAddOp(op_conf)
    lbi = logical_blob_id_util.LogicalBlobId()
    lbi.op_name = op_conf.name
    lbi.blob_name = "out"
    return remote_blob_util.RemoteBlob(lbi)


@oneflow_export("math.sigmoid")
def sigmoid(x, name=None):
    op_conf = op_conf_util.OperatorConf()
    setattr(
        op_conf, "name", name if name is not None else id_util.UniqueStr("Sigmoid_")
    )
    setattr(op_conf.sigmoid_conf, "in", x.logical_blob_name)
    setattr(op_conf.sigmoid_conf, "out", "out")
    compile_context.CurJobAddOp(op_conf)
    lbi = logical_blob_id_util.LogicalBlobId()
    lbi.op_name = op_conf.name
    lbi.blob_name = "out"
    return remote_blob_util.RemoteBlob(lbi)


def sqrt(x, name=None):
    # TODO: not ready yet
    raise NotImplementedError
    op_conf = op_conf_util.OperatorConf()
    setattr(op_conf, "name", name if name is not None else id_util.UniqueStr("Sqrt_"))
    setattr(op_conf.sqrt_conf, "in", x.logical_blob_name)
    setattr(op_conf.sqrt_conf, "out", "out")
    compile_context.CurJobAddOp(op_conf)
    lbi = logical_blob_id_util.LogicalBlobId()
    lbi.op_name = op_conf.name
    lbi.blob_name = "out"
    return remote_blob_util.RemoteBlob(lbi)


def rsqrt(x, name=None):
    # TODO: not ready yet
    raise NotImplementedError
    op_conf = op_conf_util.OperatorConf()
    setattr(op_conf, "name", name if name is not None else id_util.UniqueStr("Rsqrt_"))
    setattr(op_conf.rsqrt_conf, "in", x.logical_blob_name)
    setattr(op_conf.rsqrt_conf, "out", "out")
    compile_context.CurJobAddOp(op_conf)
    lbi = logical_blob_id_util.LogicalBlobId()
    lbi.op_name = op_conf.name
    lbi.blob_name = "out"
    return remote_blob_util.RemoteBlob(lbi)


@oneflow_export("cast")
def cast(x, dtype, name=None):
    if x.dtype == dtype:
        return x
    op_conf = op_conf_util.OperatorConf()
    setattr(op_conf, "name", name if name is not None else id_util.UniqueStr("Cast_"))
    setattr(op_conf.cast_conf, "in", x.logical_blob_name)
    setattr(op_conf.cast_conf, "data_type", dtype)
    setattr(op_conf.cast_conf, "out", "out")
    compile_context.CurJobAddOp(op_conf)
    lbi = logical_blob_id_util.LogicalBlobId()
    lbi.op_name = op_conf.name
    lbi.blob_name = "out"
    return remote_blob_util.RemoteBlob(lbi)


@oneflow_export("math.broadcast_equal")
def broadcast_equal(a, b, name=None):
    op_conf = op_conf_util.OperatorConf()
    setattr(
        op_conf,
        "name",
        name if name is not None else id_util.UniqueStr("BroadcastEqual_"),
    )
    setattr(op_conf.broadcast_equal_conf, "a", a.logical_blob_name)
    setattr(op_conf.broadcast_equal_conf, "b", b.logical_blob_name)
    setattr(op_conf.broadcast_equal_conf, "out", "out")
    compile_context.CurJobAddOp(op_conf)
    out_lbi = logical_blob_id_util.LogicalBlobId()
    setattr(out_lbi, "op_name", op_conf.name)
    setattr(out_lbi, "blob_name", "out")
    return remote_blob_util.RemoteBlob(out_lbi)


@oneflow_export("math.broadcast_not_equal")
def broadcast_not_equal(a, b, name=None):
    op_conf = op_conf_util.OperatorConf()
    setattr(
        op_conf,
        "name",
        name if name is not None else id_util.UniqueStr("BroadcastNotEqual_"),
    )
    setattr(op_conf.broadcast_not_equal_conf, "a", a.logical_blob_name)
    setattr(op_conf.broadcast_not_equal_conf, "b", b.logical_blob_name)
    setattr(op_conf.broadcast_not_equal_conf, "out", "out")
    compile_context.CurJobAddOp(op_conf)
    out_lbi = logical_blob_id_util.LogicalBlobId()
    setattr(out_lbi, "op_name", op_conf.name)
    setattr(out_lbi, "blob_name", "out")
    return remote_blob_util.RemoteBlob(out_lbi)


@oneflow_export("math.broadcast_less_than")
def broadcast_less_than(a, b, name=None):
    op_conf = op_conf_util.OperatorConf()
    setattr(
        op_conf,
        "name",
        name if name is not None else id_util.UniqueStr("BroadcastLessThan_"),
    )
    setattr(op_conf.broadcast_less_than_conf, "a", a.logical_blob_name)
    setattr(op_conf.broadcast_less_than_conf, "b", b.logical_blob_name)
    setattr(op_conf.broadcast_less_than_conf, "out", "out")
    compile_context.CurJobAddOp(op_conf)
    out_lbi = logical_blob_id_util.LogicalBlobId()
    setattr(out_lbi, "op_name", op_conf.name)
    setattr(out_lbi, "blob_name", "out")
    return remote_blob_util.RemoteBlob(out_lbi)


@oneflow_export("math.broadcast_less_equal")
def broadcast_less_equal(a, b, name=None):
    op_conf = op_conf_util.OperatorConf()
    setattr(
        op_conf,
        "name",
        name if name is not None else id_util.UniqueStr("BroadcastLessEqual_"),
    )
    setattr(op_conf.broadcast_less_equal_conf, "a", a.logical_blob_name)
    setattr(op_conf.broadcast_less_equal_conf, "b", b.logical_blob_name)
    setattr(op_conf.broadcast_less_equal_conf, "out", "out")
    compile_context.CurJobAddOp(op_conf)
    out_lbi = logical_blob_id_util.LogicalBlobId()
    setattr(out_lbi, "op_name", op_conf.name)
    setattr(out_lbi, "blob_name", "out")
    return remote_blob_util.RemoteBlob(out_lbi)


@oneflow_export("math.broadcast_greater_than")
def broadcast_greater_than(a, b, name=None):
    op_conf = op_conf_util.OperatorConf()
    setattr(
        op_conf,
        "name",
        name if name is not None else id_util.UniqueStr("BroadcastGreaterThan_"),
    )
    setattr(op_conf.broadcast_greater_than_conf, "a", a.logical_blob_name)
    setattr(op_conf.broadcast_greater_than_conf, "b", b.logical_blob_name)
    setattr(op_conf.broadcast_greater_than_conf, "out", "out")
    compile_context.CurJobAddOp(op_conf)
    out_lbi = logical_blob_id_util.LogicalBlobId()
    setattr(out_lbi, "op_name", op_conf.name)
    setattr(out_lbi, "blob_name", "out")
    return remote_blob_util.RemoteBlob(out_lbi)


@oneflow_export("math.broadcast_greater_equal")
def broadcast_greater_equal(a, b, name=None):
    op_conf = op_conf_util.OperatorConf()
    setattr(
        op_conf,
        "name",
        name if name is not None else id_util.UniqueStr("BroadcastGreaterEqual_"),
    )
    setattr(op_conf.broadcast_greater_equal_conf, "a", a.logical_blob_name)
    setattr(op_conf.broadcast_greater_equal_conf, "b", b.logical_blob_name)
    setattr(op_conf.broadcast_greater_equal_conf, "out", "out")
    compile_context.CurJobAddOp(op_conf)
    out_lbi = logical_blob_id_util.LogicalBlobId()
    setattr(out_lbi, "op_name", op_conf.name)
    setattr(out_lbi, "blob_name", "out")
    return remote_blob_util.RemoteBlob(out_lbi)


@oneflow_export("math.top_k")
def top_k(input, k=1, sorted=True, name=None):
    op_conf = op_conf_util.OperatorConf()
    setattr(op_conf, "name", name if name is not None else id_util.UniqueStr("TopK_"))
    setattr(op_conf.top_k_conf, "in", input.logical_blob_name)
    setattr(op_conf.top_k_conf, "k", k)
    setattr(op_conf.top_k_conf, "sorted", sorted)
    setattr(op_conf.top_k_conf, "out", "out")
    compile_context.CurJobAddOp(op_conf)
    out_lbi = logical_blob_id_util.LogicalBlobId()
    setattr(out_lbi, "op_name", op_conf.name)
    setattr(out_lbi, "blob_name", "out")
    return remote_blob_util.RemoteBlob(out_lbi)


@oneflow_export("math.logical_and")
def logical_and(lhs, rhs, name=None):
    op_conf = op_conf_util.OperatorConf()
    setattr(
        op_conf, "name", name if name is not None else id_util.UniqueStr("LogicalAnd_")
    )
    setattr(op_conf.logical_and_conf, "lhs", lhs.logical_blob_name)
    setattr(op_conf.logical_and_conf, "rhs", rhs.logical_blob_name)
    setattr(op_conf.logical_and_conf, "out", "out")
    compile_context.CurJobAddOp(op_conf)
    out_lbi = logical_blob_id_util.LogicalBlobId()
    setattr(out_lbi, "op_name", op_conf.name)
    setattr(out_lbi, "blob_name", "out")
    return remote_blob_util.RemoteBlob(out_lbi)


@oneflow_export("sort")
def sort(values, direction="ASCENDING", name=None):
    op_conf = op_conf_util.OperatorConf()
    setattr(op_conf, "name", name if name is not None else id_util.UniqueStr("Sort_"))
    setattr(op_conf.sort_conf, "in", values.logical_blob_name)
    setattr(op_conf.sort_conf, "dir", direction)  # "ASCENDING" or "DESCENDING"
    setattr(op_conf.sort_conf, "out", "out")
    compile_context.CurJobAddOp(op_conf)
    out_lbi = logical_blob_id_util.LogicalBlobId()
    setattr(out_lbi, "op_name", op_conf.name)
    setattr(out_lbi, "blob_name", "out")
    return remote_blob_util.RemoteBlob(out_lbi)


@oneflow_export("argsort")
def argsort(values, direction="ASCENDING", name=None):
    op_conf = op_conf_util.OperatorConf()
    setattr(
        op_conf, "name", name if name is not None else id_util.UniqueStr("Argsort_")
    )
    setattr(op_conf.arg_sort_conf, "in", values.logical_blob_name)
    setattr(op_conf.arg_sort_conf, "dir", direction)  # "ASCENDING" or "DESCENDING"
    setattr(op_conf.arg_sort_conf, "out", "out")
    compile_context.CurJobAddOp(op_conf)
    out_lbi = logical_blob_id_util.LogicalBlobId()
    setattr(out_lbi, "op_name", op_conf.name)
    setattr(out_lbi, "blob_name", "out")
    return remote_blob_util.RemoteBlob(out_lbi)
