import { useItemStore } from "../store/store";

const TotalCompleteItems = () => {
    const items = useItemStore((state) => state.items)
    const numberOfItems = items.filter((item) => item.completed).length;

    return (
        <h4 className="mt-3">Total complete items: {numberOfItems}</h4>
    )
}

export default TotalCompleteItems;