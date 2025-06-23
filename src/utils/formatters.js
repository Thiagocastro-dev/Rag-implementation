export const truncateText = (text, length = 150) => {
  if (!text) return '';
  return text.length > length ? `${text.substring(0, length)}...` : text;
};

export const formatPortariaId = (id) => {
  if (!id) return '';
  return id.replace(/\.txt$/, '').replace(/_page1$/, '');
};

export const formatDate = (dateString) => {
  try {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('pt-BR').format(date);
  } catch {
    return dateString;
  }
};