// @ts-expect-error: Could not find a declaration file for module 'react-use-keypress'.
import useKeypress from 'react-use-keypress';
import useAnyModalIsOpen from 'app/hooks/useAnyModalIsOpen.ts';
import useLookAlikesModalState from 'app/hooks/useLookAlikesModalState.ts';
import useDescribe from "components/QuickAccessPanel/hooks/useDescribe.ts";
import useRemoveText from "components/QuickAccessPanel/hooks/useRemoveText.ts";
import useOnFileDelete from "components/QuickAccessPanel/hooks/useOnFileDelete.ts";

export default function useQuickAccessHotKeys() {
    const isModalOpen = useAnyModalIsOpen();
    const { onOpenChange: openLookAlies } = useLookAlikesModalState();
    const describe = useDescribe();
    const removeTextTrigger = useRemoveText();
    const onFileDelete = useOnFileDelete();

    // Open look alikes modal
    useKeypress('l', () => {
        !isModalOpen && openLookAlies(true);
    });

    // Fast describe media
    useKeypress('d', () => {
        !isModalOpen && describe({describeMediaPayload: {prompt: ''}});
    });

    // Remove text
    useKeypress('t', () => {
        !isModalOpen && removeTextTrigger();
    });

    // Delete media
    useKeypress('Backspace', () => {
        !isModalOpen && onFileDelete();
    });
}
