"""
Copyright 2020 The OneFlow Authors. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import oneflow
from oneflow.framework.docstr.utils import add_docstr

add_docstr(
    oneflow.abs,
    r"""Return the absolute value of each element in input tensor:math:`y = |x|` element-wise.

    Args:
        input (Tensor): the input tensor.

    For example:

    .. code-block:: python

        >>> import oneflow as flow
        >>> import numpy as np

        >>> x = flow.tensor(np.array([-1, 2, -3, 4]).astype(np.float32))
        >>> flow.abs(x)
        tensor([1., 2., 3., 4.], dtype=oneflow.float32)
    
    """,
)

add_docstr(
    oneflow.add,
    r"""Computes the addition of `input` by `other` for each element, scalar and broadcast promotation are supported.
    The formula is:

    .. math::
        out = input + other

    For example:

    .. code-block:: python

        >>> import numpy as np
        >>> import oneflow as flow
        
        # element-wise add
        >>> x = flow.tensor(np.random.randn(2,3), dtype=flow.float32)
        >>> y = flow.tensor(np.random.randn(2,3), dtype=flow.float32)
        >>> out = flow.add(x, y).numpy()
        >>> out.shape
        (2, 3)

        # scalar add
        >>> x = 5
        >>> y = flow.tensor(np.random.randn(2,3), dtype=flow.float32)
        >>> out = flow.add(x, y).numpy()
        >>> out.shape
        (2, 3)

        # broadcast add
        >>> x = flow.tensor(np.random.randn(1,1), dtype=flow.float32)
        >>> y = flow.tensor(np.random.randn(2,3), dtype=flow.float32)
        >>> out = flow.add(x, y).numpy()
        >>> out.shape
        (2, 3)

    """,
)

add_docstr(
    oneflow.div,
    r"""Computes the division of input by other for each element, scalar and broadcast promotation are supported.
    The formula is:

    .. math::
        out = \\frac{input}{other}
    
    Args:
        input (Union[int, float, oneflow.Tensor]): input.
        other (Union[int, float, oneflow.Tensor]): other.
    
    For example:

    .. code-block:: python

        >>> import numpy as np
        >>> import oneflow as flow
        
        # element-wise divide
        >>> input = flow.tensor(np.random.randn(2,3), dtype=flow.float32)
        >>> other = flow.tensor(np.random.randn(2,3), dtype=flow.float32)
        >>> out = flow.div(input,other).numpy()
        >>> out.shape
        (2, 3)

        # scalar divide
        >>> input = 5
        >>> other = flow.tensor(np.random.randn(2,3), dtype=flow.float32)
        >>> out = flow.div(input,other).numpy()
        >>> out.shape
        (2, 3)

        # broadcast divide
        >>> input = flow.tensor(np.random.randn(1,1), dtype=flow.float32)
        >>> other = flow.tensor(np.random.randn(2,3), dtype=flow.float32)
        >>> out = flow.div(input,other).numpy()
        >>> out.shape 
        (2, 3)

    """,
)

add_docstr(
    oneflow.mul,
    r"""Computes the multiplication of input by other for each element, scalar and broadcast promotation are supported.
    
    The formula is:

    .. math::
        out = input \\times other
    
    For example:

    .. code-block:: python

        >>> import numpy as np
        >>> import oneflow as flow
        
        # element-wise multiply
        >>> input = flow.tensor(np.random.randn(2,3), dtype=flow.float32)
        >>> other = flow.tensor(np.random.randn(2,3), dtype=flow.float32)
        >>> out = flow.mul(input,other).numpy()
        >>> out.shape
        (2, 3)

        # scalar mutiply
        >>> input = 5
        >>> other = flow.tensor(np.random.randn(2,3), dtype=flow.float32)
        >>> out = flow.mul(input,other).numpy()
        >>> out.shape
        (2, 3)

        # broadcast mutiply
        >>> input = flow.tensor(np.random.randn(1,1), dtype=flow.float32)
        >>> other = flow.tensor(np.random.randn(2,3), dtype=flow.float32)
        >>> out = flow.mul(input,other).numpy()
        >>> out.shape 
        (2, 3)

    """,
)

add_docstr(
    oneflow.reciprocal,
    r"""Computes the safe reciprocal of x. If x is zero, the reciprocal will
    be also set to zero.

    For example:

    .. code-block:: python

        >>> import numpy as np
        >>> import oneflow as flow
        
        >>> x = flow.tensor(np.array([[1, 2, 3], [4, 5, 6]]), dtype=flow.float32)
        >>> out = flow.reciprocal(x)
        >>> out.numpy()
        array([[1.        , 0.5       , 0.33333334],
               [0.25      , 0.2       , 0.16666667]], dtype=float32)
    """,
)

add_docstr(
    oneflow.sub,
    r"""Computes the subtraction of input by other for each element, scalar and broadcast promotation are supported.
    The formula is:

    .. math::
        out = input - other
    
    For example:

    .. code-block:: python

        >>> import numpy as np
        >>> import oneflow as flow
        
        # element-wise subtract
        >>> input = flow.tensor(np.random.randn(2,3), dtype=flow.float32)
        >>> other = flow.tensor(np.random.randn(2,3), dtype=flow.float32)
        >>> out = flow.sub(input,other).numpy()
        >>> out.shape
        (2, 3)

        # scalar subtract
        >>> input = 5
        >>> other = flow.tensor(np.random.randn(2,3), dtype=flow.float32)
        >>> out = flow.sub(input,other).numpy()
        >>> out.shape
        (2, 3)

        # broadcast subtract
        >>> input = flow.tensor(np.random.randn(1,1), dtype=flow.float32)
        >>> other = flow.tensor(np.random.randn(2,3), dtype=flow.float32)
        >>> out = flow.sub(input,other).numpy()
        >>> out.shape
        (2, 3)

    """,
)

add_docstr(
    oneflow.asin,
    r"""
    Returns a new tensor with the arcsine of the elements of :attr:`input`.

    .. math::
        \\text{out}_{i} = \\sin^{-1}(\\text{input}_{i})

    Args:
        input (Tensor): the input tensor.

    For example:

    .. code-block:: python

        >>> import oneflow as flow
        >>> import numpy as np
        >>> input = flow.tensor(np.array([-0.5,  0.8, 1.0,  -0.8]), dtype=flow.float32)
        >>> output = flow.asin(input)
        >>> output.shape
        oneflow.Size([4])
        >>> output
        tensor([-0.5236,  0.9273,  1.5708, -0.9273], dtype=oneflow.float32)
        >>> input1 = flow.tensor(np.array([[0.8, 1.0], [-0.6, -1.0]]), dtype=flow.float32)
        >>> output1 = input1.asin()
        >>> output1.shape
        oneflow.Size([2, 2])
        >>> output1
        tensor([[ 0.9273,  1.5708],
                [-0.6435, -1.5708]], dtype=oneflow.float32)
    """,
)

add_docstr(
    oneflow.asinh,
    r"""
    Returns a new tensor with the inverse hyperbolic sine of the elements of :attr:`input`.

    .. math::
        \\text{out}_{i} = \\sinh^{-1}(\\text{input}_{i})

    Args:
        input (Tensor): the input tensor.

    For example:

    .. code-block:: python

        >>> import oneflow as flow
        >>> import numpy as np
        >>> input = flow.tensor(np.array([2, 3, 4]), dtype=flow.float32)
        >>> output = flow.asinh(input)
        >>> output.shape
        oneflow.Size([3])
        >>> output
        tensor([1.4436, 1.8184, 2.0947], dtype=oneflow.float32)

        >>> input1 = flow.tensor(np.array([[-1, 0, -0.4], [5, 7, 0.8]]), dtype=flow.float32)
        >>> output1 = input1.asinh()
        >>> output1.shape
        oneflow.Size([2, 3])
        >>> output1
        tensor([[-0.8814,  0.0000, -0.3900],
                [ 2.3124,  2.6441,  0.7327]], dtype=oneflow.float32)

    """,
)

add_docstr(
    oneflow.atan,
    r"""
    Returns a new tensor with the arctangent of the elements of :attr:`input`.

    .. math::
        \\text{out}_{i} = \\tan^{-1}(\\text{input}_{i})

    Args:
        input (Tensor): the input tensor.

    For example:

    .. code-block:: python
    
        >>> import oneflow as flow
        >>> import numpy as np
        >>> input = flow.tensor(np.array([0.5, 0.6, 0.7]), dtype=flow.float32)
        >>> output = flow.atan(input)
        >>> output.shape
        oneflow.Size([3])
        
    """,
)

add_docstr(
    oneflow.ceil,
    r"""Returns a new tensor with the ceil of the elements of :attr:`input`,
    the smallest integer greater than or equal to each element.

    The equation is: 

    .. math::
        \\text{out}_{i} = \\left\\lceil \\text{input}_{i} \\right\\rceil = \\left\\lfloor \\text{input}_{i} \\right\\rfloor + 1

    Args:
        input (oneflow.Tensor): A Tensor.
    
    Returns:
        oneflow.Tensor: The result Tensor

    For example: 


    .. code-block:: python 
        
        >>> import oneflow as flow
        >>> import numpy as np   
        >>> x = flow.tensor(np.array([0.1, -2, 3.4]).astype(np.float32))
        >>> y = flow.ceil(x)
        >>> y.shape
        oneflow.Size([3])
        >>> y
        tensor([ 1., -2.,  4.], dtype=oneflow.float32)
        >>> x = flow.tensor(np.array([[2.5, 4.6, 0.6],[7.8, 8.3, 9.2]]).astype(np.float32))
        >>> y = x.ceil()
        >>> y.shape
        oneflow.Size([2, 3])
        >>> y
        tensor([[ 3.,  5.,  1.],
                [ 8.,  9., 10.]], dtype=oneflow.float32)
        >>> x = flow.tensor(np.array([[[2.2, 4.4, 6.5],[7.1, 8.2, 9.3]],[[10.6,11.2,12.2],[13.5,14.8,15.9]]]).astype(np.float32))
        >>> y = flow.ceil(x)
        >>> y.shape
        oneflow.Size([2, 2, 3])
        >>> y
        tensor([[[ 3.,  5.,  7.],
                 [ 8.,  9., 10.]],
        <BLANKLINE>
                [[11., 12., 13.],
                 [14., 15., 16.]]], dtype=oneflow.float32)

    """,
)

add_docstr(
    oneflow.log1p,
    r"""Returns a new tensor with the natural logarithm of (1 + input).

    .. math::
        \\text{out}_{i}=\\log_e(1+\\text{input}_{i})

    For example:

    .. code-block:: python

        >>> import oneflow as flow
        >>> import numpy as np
        >>> x = flow.tensor(np.array([1.3, 1.5, 2.7]), dtype=flow.float32)
        >>> out = flow.log1p(x)
        >>> out
        tensor([0.8329, 0.9163, 1.3083], dtype=oneflow.float32)

    """,
)

add_docstr(
    oneflow.exp,
    r"""

    This operator computes the exponential of Tensor.

    The equation is:

    .. math::

        out = e^x

    Args:
        x (oneflow.Tensor): A Tensor

    Returns:
        oneflow.Tensor: The result Tensor

    For example:

    .. code-block:: python

        >>> import numpy as np
        >>> import oneflow as flow
        
        >>> x = flow.tensor(np.array([1, 2, 3]).astype(np.float32), dtype=flow.float32)
        >>> y = flow.exp(x)
        >>> y
        tensor([ 2.7183,  7.3891, 20.0855], dtype=oneflow.float32)

    """,
)

add_docstr(
    oneflow.acos,
    r"""
    Returns a new tensor with the inverse cosine of the elements of :attr:`input`.

    .. math::
        \\text{out}_{i} = \\arccos(\\text{input}_{i})

    Args:
        input (Tensor): the input tensor.

    For example:

    .. code-block:: python

        >>> import oneflow as flow
        >>> import numpy as np

        >>> arr = np.array([0.5, 0.6, 0.7])
        >>> input = flow.tensor(arr, dtype=flow.float32)
        >>> output = flow.acos(input)
        >>> output
        tensor([1.0472, 0.9273, 0.7954], dtype=oneflow.float32)
    """,
)

add_docstr(
    oneflow.acosh,
    r"""
    Returns a new tensor with the inverse hyperbolic cosine of the elements of :attr:`input`.

    .. math::

        \\text{out}_{i} = \\cosh^{-1}(\\text{input}_{i})

    Args:
        input (Tensor): the input tensor.

    For example:

    .. code-block:: python

        >>> import oneflow as flow
        >>> import numpy as np
        >>> x1 = flow.tensor(np.array([2, 3, 4]).astype(np.float32))
        >>> out1 = flow.acosh(x1)
        >>> out1
        tensor([1.3170, 1.7627, 2.0634], dtype=oneflow.float32)
        >>> x2 = flow.tensor(np.array([1.5, 2.6, 3.7]).astype(np.float32),device=flow.device('cuda'))
        >>> out2 = flow.acosh(x2)
        >>> out2
        tensor([0.9624, 1.6094, 1.9827], device='cuda:0', dtype=oneflow.float32)
    """,
)

add_docstr(
    oneflow.atanh,
    r"""Returns a new tensor with the inverse hyperbolic tangent of the elements of :attr:`input`.

    .. math::
        \\text{out}_{i} = \\tanh^{-1}(\\text{input}_{i})

    Args:
        input (Tensor): the input tensor.

    For example:

    .. code-block:: python

        >>> import oneflow as flow
        >>> import numpy as np
        >>> np_arr = np.array([0.5, 0.6, 0.7]).astype(np.float32)
        >>> input = flow.tensor(np_arr, dtype=flow.float32)
        >>> output = flow.atanh(input)
        >>> output
        tensor([0.5493, 0.6931, 0.8673], dtype=oneflow.float32)

    """,
)

add_docstr(
    oneflow.sign,
    r"""Computes the sign of Tensor.

    .. math::

        \\text{out}_{i}  = \\text{sgn}(\\text{input}_{i})

    Args:
        input (Tensor): the input tensor.

    For example:

    .. code-block:: python

        >>> import oneflow as flow
        >>> import numpy as np
        >>> x1 = flow.tensor(np.array([-2, 0, 2]).astype(np.float32))
        >>> out1 = flow.sign(x1)
        >>> out1.numpy()
        array([-1.,  0.,  1.], dtype=float32)
        >>> x2 = flow.tensor(np.array([-3.2, -4.5, 5.8]).astype(np.float32),device=flow.device('cuda'))
        >>> out2 = flow.sign(x2)
        >>> out2.numpy()
        array([-1., -1.,  1.], dtype=float32)

    """,
)

add_docstr(
    oneflow.sin,
    r"""Returns a new tensor with the sine of the elements of :attr:`input`.

    sin(x: Tensor) -> Tensor
    
    .. math::
        \text{y}_{i} = \sin(\text{x}_{i})
    
    Args:
        x (Tensor): the input tensor.
        
    For example:
    .. code-block:: python

        >>> import oneflow as flow
        >>> import numpy as np
        >>> x1 = flow.tensor(np.array([-0.5461,  0.1347, -2.7266, -0.2746]).astype(np.float32))
        >>> y1 = flow.sin(x1)
        >>> y1
        tensor([-0.5194,  0.1343, -0.4032, -0.2712], dtype=oneflow.float32)
        
        >>> x2 = flow.tensor(np.array([-1.4, 2.6, 3.7]).astype(np.float32), device=flow.device('cuda'))
        >>> y2 = flow.sin(x2)
        >>> y2
        tensor([-0.9854,  0.5155, -0.5298], device='cuda:0', dtype=oneflow.float32)
        
    """,
)

add_docstr(
    oneflow.sin_,
    r"""
    In-place version of :func:`oneflow.sin`

    """,
)

add_docstr(
    oneflow.sinh,
    r"""Returns a new tensor with the hyperbolic sine of the elements of :attr:`input`.

    .. math::
        \\text{out}_{i} = \\sinh(\\text{input}_{i})

    Args:
        input (Tensor): the input tensor.

    For example:

    .. code-block:: python

        >>> import numpy as np
        >>> import oneflow as flow

        >>> x1 = flow.tensor(np.array([1, 2, 3]), dtype=flow.float32)
        >>> x2 = flow.tensor(np.array([1.53123589,0.54242598,0.15117185]), dtype=flow.float32)
        >>> x3 = flow.tensor(np.array([1,0,-1]), dtype=flow.float32)

        >>> flow.sinh(x1).numpy()
        array([ 1.1752012,  3.6268604, 10.017875 ], dtype=float32)
        >>> flow.sinh(x2).numpy()
        array([2.20381  , 0.5694193, 0.1517483], dtype=float32)
        >>> flow.sinh(x3).numpy()
        array([ 1.1752012,  0.       , -1.1752012], dtype=float32)

    """,
)

add_docstr(
    oneflow.tan,
    r"""Returns  the tan value of the elements of :attr:`input`.

    .. math::
        \\text{out}_{i} = \\tan(\\text{input}_{i})

    Args:
        input (Tensor): the input tensor.

    For example:

    .. code-block:: python

        >>> import oneflow as flow
        >>> import numpy as np
        >>> np_arr = np.array([-1/4*np.pi, 0, 1/4*np.pi]).astype(np.float32)
        >>> input = flow.tensor(np_arr, dtype=flow.float32)
        >>> output = flow.tan(input)
        >>> output
        tensor([-1.,  0.,  1.], dtype=oneflow.float32)

    """,
)

add_docstr(
    oneflow.clamp,
    r"""
    Clamp all elements in :attr:`input` into the range `[` :attr:`min`, :attr:`max` `]` and return
    a resulting tensor:

    .. math::
        y_i = \\begin{cases}
            \\text{min} & \\text{if } x_i < \\text{min} \\\\
            x_i & \\text{if } \\text{min} \\leq x_i \\leq \\text{max} \\\\
            \\text{max} & \\text{if } x_i > \\text{max}
        \\end{cases}

    If :attr:`input` is of type `FloatTensor` or `DoubleTensor`, args :attr:`min`
    and :attr:`max` must be real numbers, otherwise they should be integers.

    Args:
        input (Tensor): the input tensor.
        min (Number): lower-bound of the range to be clamped to. Defaults to None.
        max (Number): upper-bound of the range to be clamped to. Defaults to None.
        out (Tensor, optional): the output tensor.

    For example:


    .. code-block:: python

        >>> import oneflow as flow
        >>> import numpy as np
        >>> arr = np.array([0.2, 0.6, -1.5, -0.3])
        >>> input = flow.tensor(arr, dtype=flow.float32)
        >>> output = flow.clamp(input, min=-0.5, max=0.5)
        >>> output
        tensor([ 0.2000,  0.5000, -0.5000, -0.3000], dtype=oneflow.float32)

        >>> arr = np.array([0.2, 0.6, -1.5, -0.3])
        >>> input = flow.tensor(arr, dtype=flow.float32)
        >>> output = flow.clamp(input, min=None, max=0.5)
        >>> output
        tensor([ 0.2000,  0.5000, -1.5000, -0.3000], dtype=oneflow.float32)

        >>> arr = np.array([0.2, 0.6, -1.5, -0.3])
        >>> input = flow.tensor(arr, dtype=flow.float32)
        >>> output = flow.clamp(input, min=-0.5, max=None)
        >>> output
        tensor([ 0.2000,  0.6000, -0.5000, -0.3000], dtype=oneflow.float32)

    """,
)

add_docstr(
    oneflow.cos,
    r"""
    Returns a new tensor with the cosine  of the elements of :attr:`input`.
    
    .. math::
        \\text{out}_{i} = \\cos(\\text{input}_{i})

    Args:
        input (Tensor): the input tensor.

    For example:

    .. code-block:: python

        >>> import oneflow as flow
        >>> import numpy as np
        >>> arr = np.array([1.4309,  1.2706, -0.8562,  0.9796])
        >>> input = flow.tensor(arr, dtype=flow.float32)
        >>> output = flow.cos(input).numpy()

    """,
)

add_docstr(
    oneflow.cosh,
    r"""
    Returns a new tensor with the hyperbolic cosine of the elements of :attr:`input`.

    .. math::
        \\text{out}_{i} = \\cosh(\\text{input}_{i})

    Args:
        input (Tensor): the input tensor.

    For example:

    .. code-block:: python

        >>> import numpy as np
        >>> import oneflow as flow
        
        >>> arr = np.array([ 0.1632,  1.1835, -0.6979, -0.7325])
        >>> input = flow.tensor(arr, dtype=flow.float32)
        >>> output = flow.cosh(input).numpy()
        >>> output
        array([1.0133467, 1.7859949, 1.2535787, 1.2804903], dtype=float32)

    """,
)

add_docstr(
    oneflow.erf,
    r"""Computes the error function of each element. The error function is defined as follows:

    .. math::
            \\operatorname{erf}(x)=\\frac{2}{\\sqrt{\\pi}} \\int_{0}^{x} e^{-t^{2}} d t

    Args:
        x (oneflow.Tensor): A Tensor

    Returns:
        oneflow.Tensor: The result Tensor   
               
    For example:

    .. code-block:: python

        >>> import oneflow as flow
        >>> import numpy as np
        
        >>> x = flow.tensor(np.array([0, -1., 10.]), dtype=flow.float32)
        >>> out = flow.erf(x)
        >>> out.shape
        oneflow.Size([3])
        >>> out.numpy()
        array([ 0.       , -0.8427008,  1.       ], dtype=float32)

        >>> x = flow.tensor(np.array([[0, -1., 10.], [5, 7, 0.8]]), dtype=flow.float32)
        >>> out = flow.erf(x)
        >>> out.shape
        oneflow.Size([2, 3])
        >>> out.numpy()
        array([[ 0.        , -0.8427008 ,  1.        ],
               [ 1.        ,  1.        ,  0.74210095]], dtype=float32)

        >>> x = flow.tensor(np.array([[0, -1., 10.], [5, 7, 0.8], [2, 3, 4]]), dtype=flow.float32)
        >>> out = x.erf()
        >>> out.shape
        oneflow.Size([3, 3])
        >>> out.numpy()
        array([[ 0.        , -0.8427008 ,  1.        ],
               [ 1.        ,  1.        ,  0.74210095],
               [ 0.9953223 ,  0.9999779 ,  1.        ]], dtype=float32)

    """,
)

add_docstr(
    oneflow.erfc,
    r"""Computes the complementary error function of each element of input. The complementary error 
    function is defined as follows:

    .. math::
            \\operatorname{erfc}(x)=1-\\frac{2}{\\sqrt{\\pi}} \\int_{0}^{x} e^{-t^{2}} d t

    Args:
        x (oneflow.Tensor): A Tensor

    Returns:
        oneflow.Tensor: The result Tensor

    For example:

    .. code-block:: python

        >>> import oneflow as flow
        >>> import numpy as np
        
        >>> x = flow.tensor(np.array([0, -1., 10.]), dtype=flow.float32)
        >>> out = flow.erfc(x)
        >>> out
        tensor([1.0000e+00, 1.8427e+00, 2.8026e-45], dtype=oneflow.float32)

        >>> x = flow.tensor(np.array([[0, -1., 10.], [5, 7, 0.8]]), dtype=flow.float32)
        >>> out = flow.erfc(x)
        >>> out
        tensor([[1.0000e+00, 1.8427e+00, 2.8026e-45],
                [1.5375e-12, 4.1838e-23, 2.5790e-01]], dtype=oneflow.float32)
        
    """,
)

add_docstr(
    oneflow.expm1,
    r"""Returns a new tensor with the exponential of the elements minus 1
    of :attr:`input`.


    The equation is: 

    .. math::
        y_{i} = e^{x_{i}} - 1

    Args:
        input (oneflow.Tensor): A Tensor.
    
    Returns:
        oneflow.Tensor: The result Tensor

    For example: 

    .. code-block:: python 
        
        >>> import oneflow as flow
        >>> import numpy as np
        >>> x = flow.tensor(np.array([1, 2, 3]).astype(np.float32))
        >>> y = flow.expm1(x)
        >>> y.shape
        oneflow.Size([3])
        >>> y
        tensor([ 1.7183,  6.3891, 19.0855], dtype=oneflow.float32)

        >>> x = flow.tensor(np.array([[[2, 4, 6],[7, 8, 9]],[[10,11,12],[13,14,15]]]).astype(np.float32))
        >>> y = flow.expm1(x)
        >>> print(y.shape)
        oneflow.Size([2, 2, 3])
        >>> print(y.numpy())
        [[[6.3890562e+00 5.3598152e+01 4.0242880e+02]
          [1.0956332e+03 2.9799580e+03 8.1020840e+03]]
        <BLANKLINE>
         [[2.2025465e+04 5.9873141e+04 1.6275380e+05]
          [4.4241238e+05 1.2026032e+06 3.2690165e+06]]]


    """,
)

add_docstr(
    oneflow.fmod,
    r"""
    fmod(input, other, *, out=None) -> Tensor

    Computes the element-wise remainder of division.

    The dividend and divisor may contain both for integer and floating point
    numbers. The remainder has the same sign as the dividend :attr:`input`.

    Supports broadcasting to a common shape, integer and float inputs.


    Args:
        input (Tensor): the dividend
        other (Tensor or Scalar): the divisor

    Keyword args:
        out (Tensor, optional): the output tensor.

    Example::

        >>> import oneflow as flow
        >>> flow.fmod(flow.tensor([-3., -2, -1, 1, 2, 3], dtype=flow.float32), 2.)
        tensor([-1., -0., -1.,  1.,  0.,  1.], dtype=oneflow.float32)
        >>> flow.fmod(flow.tensor([1, 2, 3, 4, 5.], dtype=flow.float32), 1.5)
        tensor([1.0000, 0.5000, 0.0000, 1.0000, 0.5000], dtype=oneflow.float32)
        >>> flow.fmod(flow.tensor([1, 2, 3, 4., -5]), flow.tensor([4, 2, 1, 3., 1]))
        tensor([1., 0., 0., 1., -0.], dtype=oneflow.float32)

    """,
)

add_docstr(
    oneflow.log,
    r"""
    Returns a new tensor with the natural logarithm of the elements of :attr:`input`.
    
    .. math::
        y_{i} = \\log_{e} (x_{i})

    Args:
        input (Tensor): the input tensor.
    
    For example:

    .. code-block:: python

        >>> import oneflow as flow
        >>> import numpy as np
        >>> arr = np.random.randn(2, 3, 4, 5)
        >>> input = flow.tensor(arr, dtype=flow.float32)
        >>> output = flow.log(input)


    """,
)

add_docstr(
    oneflow.minimum,
    r"""Computes the element-wise minimum of x and y.

    For example:

    .. code-block:: python

        >>> import numpy as np
        >>> import oneflow as flow

        >>> x = flow.tensor((1, 2, -1), dtype=flow.float32)
        >>> y = flow.tensor((3, 0, 4), dtype=flow.float32)
        >>> flow.minimum(x, y)
        tensor([ 1.,  0., -1.], dtype=oneflow.float32)

        >>> x = flow.tensor((1,), dtype=flow.float32)
        >>> y = flow.tensor((3, 0, 4), dtype=flow.float32)
        >>> flow.minimum(x, y)
        tensor([1., 0., 1.], dtype=oneflow.float32)
    """,
)

add_docstr(
    oneflow.maximum,
    r"""Computes the element-wise maximum of x and y.

    For example:

    .. code-block:: python

        >>> import numpy as np
        >>> import oneflow as flow

        >>> x = flow.tensor((1, 2, -1), dtype=flow.float32)
        >>> y = flow.tensor((3, 0, 4), dtype=flow.float32)
        >>> flow.maximum(x, y)
        tensor([3., 2., 4.], dtype=oneflow.float32)

        >>> x = flow.tensor((1,), dtype=flow.float32)
        >>> y = flow.tensor((3, 0, 4), dtype=flow.float32)
        >>> flow.maximum(x, y)
        tensor([3., 1., 4.], dtype=oneflow.float32)
    """,
)

add_docstr(
    oneflow.pow,
    r"""Takes the power of each element in input with exponent and returns a tensor with the result. Exponent can be either a single float number, a single int number, or a tensor with the same shape as input.
    When exponent is a scalar value, the operation applied is:

    .. math::
        \\text{out}_i = x_i ^ \\text{exponent}
\u200b
    When exponent is a tensor, the operation applied is:

    .. math::
        \\text{out}_i = x_i ^ {\\text{exponent}_i}

    Args:
        - input (Tensor): the input tensor.
        - exponent (int, float, Tensor): the exponent.

    Returns:
        Tensor: The result of variance on the specified axis of input Tensor

    For example:

    .. code-block:: python

        >>> import oneflow as flow
        >>> import numpy as np
        
        >>> x = flow.tensor(np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0]), dtype=flow.float32)
        >>> out = flow.pow(x, 2)
        >>> out
        tensor([ 1.,  4.,  9., 16., 25., 36.], dtype=oneflow.float32)

        >>> x = flow.tensor(np.array([1.0, 2.0, 3.0, 4.0]), dtype=flow.float32)
        >>> y = flow.tensor(np.array([1.0, 2.0, 3.0, 4.0]), dtype=flow.float32)
        >>> out = flow.pow(x, y)
        >>> out
        tensor([  1.,   4.,  27., 256.], dtype=oneflow.float32)
        
    """,
)

add_docstr(
    oneflow.rsqrt,
    r"""Returns a new tensor with the reciprocal of the square-root of each of
        the elements of :attr:`input`.

        .. math::
            \\text{out}_{i} = \\frac{1}{\\sqrt{\\text{input}_{i}}}

        Args:
            input (Tensor): the input tensor.

         For example:

        .. code-block:: python

            >>> import oneflow as flow
            >>> import numpy as np
            
            >>> a = flow.tensor(np.array([1.0, 2.0, 3.0]), dtype=flow.float32)
            >>> out = flow.rsqrt(a).numpy()
            >>> out
            array([1.        , 0.70710677, 0.57735026], dtype=float32)
    """,
)

add_docstr(
    oneflow.sqrt,
    r"""Returns a new tensor with the square-root of the elements of :attr:`input`.

        .. math::
            \\text{out}_{i} = \\sqrt{\\text{input}_{i}}

        Args:
            input (Tensor): the input tensor.

         For example:

        .. code-block:: python

            >>> import oneflow as flow
            >>> import numpy as np
            
            >>> arr = np.array([1.0, 2.0, 3.0])
            >>> input = flow.tensor(arr, dtype=flow.float32)
            >>> output = flow.sqrt(input).numpy()
            >>> output
            array([1.       , 1.4142135, 1.7320508], dtype=float32)
        """,
)


add_docstr(
    oneflow.square,
    r"""Returns a new tensor with the square of the elements of :attr:`input`.

        .. math::
            \\text{out}_{i} = \\sqrt{\\text{input}_{i}}

        Args:
            input (Tensor): the input tensor.

         For example:

        .. code-block:: python

            >>> import oneflow as flow
            >>> import numpy as np
            
            >>> arr = np.array([1.0, 2.0, 3.0])
            >>> input = flow.tensor(arr, dtype=flow.float32)
            >>> output = flow.square(input).numpy()
            >>> output
            array([1., 4., 9.], dtype=float32)
        """,
)

add_docstr(
    oneflow.matmul,
    r"""This operator applies matrix multiplication to two Tensor.

    Args:
        a (oneflow.Tensor): A Tensor
        b (oneflow.Tensor): A Tensor

    Returns:
        oneflow.Tensor: The result Tensor

    For example:

    .. code-block:: python

        >>> import oneflow as flow
        >>> import numpy as np
        >>> input1 = flow.tensor(np.random.randn(2, 6), dtype=flow.float32)
        >>> input2 = flow.tensor(np.random.randn(6, 5), dtype=flow.float32)
        >>> of_out = flow.matmul(input1, input2)
        >>> of_out.shape
        oneflow.Size([2, 5])

    """,
)

add_docstr(
    oneflow.round,
    r"""This operator rounds the value of Blob to the nearest integer.
    Args:
        input (oneflow.Tensor): A Tensor
    Returns:
        oneflow.Tensor: The result Tensor
    For example:

    .. code-block:: python

        >>> import oneflow as flow
        >>> import numpy as np
        >>> x1 = flow.tensor(np.array([1.49999, 1.500001, 2.7]).astype(np.float32))
        >>> out1 = flow.round(x1)
        >>> out1.numpy()
        array([1., 2., 3.], dtype=float32)
        >>> x2 = flow.tensor(np.array([2.499999, 7.5000001, 5.3, 6.8]).astype(np.float32))
        >>> out2 = flow.round(x2)
        >>> out2.numpy()
        array([2., 8., 5., 7.], dtype=float32)

    """,
)

add_docstr(
    oneflow.std,
    r"""
    Returns the standard-deviation of each row of the :attr:`input` tensor in the
    dimension :attr:`dim`. If :attr:`dim` is a list of dimensions,
    reduce over all of them.

    If keepdim is True, the output tensor is of the same size as input except in 
    the dimension(s) dim where it is of size 1. Otherwise, dim is squeezed, 
    resulting in the output tensor having 1 (or len(dim)) fewer dimension(s).

    If :attr:`unbiased` is ``False``, then the standard-deviation will be calculated
    via the biased estimator. Otherwise, Bessel's correction will be used.

    Args:
        input (Tensor): the input tensor.
        dim (int or tuple of python:ints): the dimension or dimensions to reduce.
        unbiased (bool): whether to use the unbiased estimation or not
        keepdim (bool): whether the output tensor has `dim` retained or not.

    For example:

    .. code-block:: python

        >>> import oneflow as flow
        >>> import numpy as np
        
        >>> arr = np.array([1.0, 2.0, 3.0])
        >>> input = flow.tensor(arr)
        >>> output = flow.std(input, dim=0).numpy()
        >>> output
        array(1.)

    """,
)

add_docstr(
    oneflow.var,
    r"""Returns the variance of each row of the `input` tensor in the given dimension `dim`.

    If `keepdim` is `True`, the output tensor is of the same size as `input` except in the dimension(s) `dim` 
    where it is of size 1. Otherwise, dim is squeezed (see `flow.squeeze()`), resulting in the output 
    tensor having 1 (or `len(dim)`) fewer dimension(s).

    Args:
        input (Tensor): the input tensor.
        dim (int or tuple of python:ints): the dimension or dimensions to reduce. Defaults to None.
        unbiased (bool, optional): whether to use Bessel’s correction (:math:`\delta N = 1`). Defaults to True.
        keepdim (bool, optional): whether the output tensor has dim retained or not. Defaults to False.

    Returns:
        Tensor: The result of variance on the specified axis of input Tensor

    For example:

    .. code-block:: python

        >>> import numpy as np
        >>> import oneflow as flow
        
        >>> input = flow.tensor(np.random.randn(2, 3, 4, 5))
        >>> output = flow.var(input, 1, True)

    """,
)