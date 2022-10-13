export function Prettify(str: string) {
  str = str.replace(/[_]/g, " ");
  str = str.replace(/(^\w)|([-\s]\w)/g, match => match.toUpperCase());
  console.log(str);
  return str;
}