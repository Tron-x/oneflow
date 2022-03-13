#include <type_traits>

#include <pybind11/pybind11.h>

namespace pybind11 {
namespace detail {

// The condition follows the pybind11 source code
template<typename T>
using IsSupportedByPybind11WhenInsideSharedPtr =
    std::is_base_of<type_caster_base<T>, type_caster<T>>;

}
}  // namespace pybind11
