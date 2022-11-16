export function Prettify(str: string) {
  const standards: { [key: string]: string } = {
    "name_first": "First Name",
    "name_last": "Last Name",
  }
  if (Object.keys(standards).includes(str)) return standards[str];
  str = str.replace(/[_]/g, " ");
  str = str.replace(/(^\w)|([-\s]\w)/g, match => match.toUpperCase());
  return str;
}
