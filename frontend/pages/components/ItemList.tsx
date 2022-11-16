import styled from '@emotion/styled'
import { Flex } from 'theme-ui'
import {theme} from '../../theme'

type Props<T> = { items: T[], getItemKey:(item: T)=> React.Key | null | undefined, getItemLabel: (item: T) => string, onClickItem: (item: T) => void, selectedItem: T|null,}

const ItemList = <T,>({ items, getItemKey, getItemLabel, onClickItem, selectedItem }: Props<T>) => {
  
  const SelectedDiv = styled.div `
    height: 3rem;
    width: 10rem;
    margin: 0.2rem;
    text-align: center;
    padding-top: 1.5rem;
    border-radius: 0.5rem;
    &.buttonSelected {
      background-color: lightgray;
    }
    
    &:hover {
      background-color: ${theme.colors?.highlight}
    }
  `
  return (
    <Flex sx={{ flexDirection: 'column' , alignItems: 'center'}}>
    
      {items.map((item) => {
        return <SelectedDiv className = {selectedItem != null && getItemKey(selectedItem) === getItemKey(item)? 'buttonSelected': ''} key={getItemKey(item)} onClick={() => { onClickItem(item);}} >
          {getItemLabel(item)}
        </SelectedDiv>
      })}
    </Flex>
  )
}

export default ItemList
