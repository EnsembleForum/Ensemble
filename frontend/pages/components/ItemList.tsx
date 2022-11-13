import { Flex } from 'theme-ui'

type Props<T> = { items: T[], getItemKey:(item: T)=> React.Key | null | undefined, getItemLabel: (item: T) => string, onClickItem: (item: T) => void }

const ItemList = <T,>({ items, getItemKey, getItemLabel, onClickItem }: Props<T>) => {
  return (
    <Flex sx={{ flexDirection: 'column' }}>
      {items.map((item) => {
        return <div key={getItemKey(item)} onClick={() => { onClickItem(item) }}>
          {getItemLabel(item)}
        </div>
      })}
    </Flex>
  )
}

export default ItemList
