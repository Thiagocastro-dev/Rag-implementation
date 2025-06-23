export const calculatePagination = (currentPage, totalItems, itemsPerPage) => {
  return {
    totalPages: Math.ceil(totalItems / itemsPerPage),
    startIndex: (currentPage - 1) * itemsPerPage,
    endIndex: Math.min(currentPage * itemsPerPage, totalItems),
    hasNextPage: currentPage * itemsPerPage < totalItems,
    hasPreviousPage: currentPage > 1
  };
};