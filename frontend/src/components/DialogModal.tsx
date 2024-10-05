// @ts-expect-error: Could not find a declaration file for module 'react-use-keypress'.
import useKeypress from 'react-use-keypress';
import { Button, Modal, ModalBody, ModalContent, ModalFooter, ModalHeader } from '@nextui-org/react';
import { useDispatch, useSelector } from 'react-redux';
import { selectDialog, setDialog } from 'app/slices/appSlice.ts';
import { useCallback } from 'react';

const baseDialogState = {
    isOpen: false,
    title: '',
    content: '',
    confirmed: false,
};

export default function DialogModal() {
    const dispatch = useDispatch();
    const dialogState = useSelector(selectDialog);

    const onClose = useCallback(() => {
        dispatch(setDialog(baseDialogState));
    }, [dispatch]);

    const onConfirm = useCallback(() => {
        dispatch(setDialog({ ...baseDialogState, confirmed: true }));
    }, [dispatch]);

    useKeypress('Enter', () => {
        dialogState.isOpen && onConfirm();
    });

    useKeypress('Escape', () => {
        dialogState.isOpen && onClose();
    });

    return (
        <Modal isOpen={dialogState.isOpen} onClose={onClose} className="self-center z-1000">
            <ModalContent>
                <ModalHeader className="flex flex-row w-full justify-center">{dialogState.title}</ModalHeader>
                <ModalBody className="text-center">{dialogState.content || ''}</ModalBody>
                <ModalFooter className="flex flex-inline gap-20 justify-center">
                    <Button onPress={onClose}>Cancel</Button>
                    <Button color="primary" onPress={onConfirm}>
                        Confirm
                    </Button>
                </ModalFooter>
            </ModalContent>
        </Modal>
    );
}
