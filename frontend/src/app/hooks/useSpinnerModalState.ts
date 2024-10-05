import {useDispatch, useSelector} from "react-redux";
import {selectSpinnerModal, setSpinnerModalIsOpen} from "app/slices/appSlice.ts";
import {useCallback} from "react";

export default function useSpinnerModalState() {
    const dispatch = useDispatch();
    const state = useSelector(selectSpinnerModal);

    const onOpenChange = useCallback((isOpen: boolean) => {
        dispatch(setSpinnerModalIsOpen(isOpen));
    }, [dispatch]);

    return {
        isOpen: state.isOpen,
        onOpenChange,
    }
}
