
export function Prettify(str: string) {
  const standards: { [key: string]: string } = {
    "name_first": "First Name",
    "name_last": "Last Name",
  }
  if (str in Object.keys(standards)) return standards[str];
  str = str.replace(/[_]/g, " ");
  str = str.replace(/(^\w)|([-\s]\w)/g, match => match.toUpperCase());
  return str;
}
