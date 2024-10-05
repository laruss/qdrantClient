import { Button, Dropdown, DropdownItem, DropdownMenu, DropdownTrigger, Input } from '@nextui-org/react';
import { useCallback, useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import { selectDescriptionData } from 'app/slices/appSlice.ts';
import useSetDescriptionMutation from './hooks/useSetDescriptionMutation.ts';
import useDescribeMutation from 'components/DescriptionModal/hooks/useDescribeMutation.ts';
import { GoGear } from 'react-icons/go';
import PromptsModal from 'components/DescriptionModal/PromptsModal.tsx';
import usePromptItems from 'components/DescriptionModal/hooks/usePromptItems.ts';

type DescriptionPromptProps = {
    onSavedCallback: () => unknown;
    onLoadingCallback: () => unknown;
    onDescribedCallback: () => unknown;
};

export default function DescriptionPrompt({
                                              onSavedCallback,
                                              onLoadingCallback,
                                              onDescribedCallback,
                                          }: DescriptionPromptProps) {
    const descriptionData = useSelector(selectDescriptionData);
    const [prompt, setPrompt] = useState<string>('');
    const {
        saveDescription,
        isDescriptionSaved,
        isDescriptionSaving,
    } = useSetDescriptionMutation();
    const {
        describe,
        isDescribed,
        isDescribing,
    } = useDescribeMutation();
    const [isPromptModalOpen, setIsPromptModalOpen] = useState<boolean>(false);
    const [promptItems, setPromptItems] = usePromptItems();

    const isLoading = isDescriptionSaving || isDescribing;

    const onSave = useCallback(() => {
        saveDescription({ imageDescription: descriptionData! });
    }, [descriptionData, saveDescription]);

    const onDescribe = useCallback(() => {
        describe({ describeMediaPayload: { prompt } });
    }, [describe, prompt]);

    useEffect(() => {
        if (isDescriptionSaved) {
            onSavedCallback();
        }
    }, [isDescriptionSaved, onSavedCallback]);

    useEffect(() => {
        if (isLoading) {
            onLoadingCallback();
        }
    }, [isLoading, onLoadingCallback]);

    useEffect(() => {
        if (isDescribed) {
            onDescribedCallback();
        }
    }, [isDescribed, onDescribedCallback]);

    return (
        <div className="w-2/3 flex flex-col gap-5">
            <Input
                label="Prompt"
                className="w-full"
                onChange={(e) => setPrompt(e.target.value)}
                isClearable
                onClear={() => setPrompt('')}
                isDisabled={isLoading}
                value={prompt}
            />
            <div className="w-full inline-flex justify-center gap-1">
                <Dropdown>
                    <DropdownTrigger>
                        <Button className="w-3/4">Additional Prompts</Button>
                    </DropdownTrigger>
                    <DropdownMenu
                        aria-label="Additional Prompts"
                        items={
                            promptItems.map((item, index) => ({
                                key: index,
                                label: item,
                            }))
                        }
                    >
                        {
                            item => (
                                <DropdownItem
                                    key={item.key}
                                    onClick={() => setPrompt(prompt => prompt.trim() + ' ' + item.label)}
                                >
                                    {item.label}
                                </DropdownItem>
                            )
                        }
                    </DropdownMenu>
                </Dropdown>
                <Button isIconOnly onPress={() => setIsPromptModalOpen(true)}>
                    <GoGear />
                </Button>
            </div>
            <div className="w-full flex flex-row justify-stretch flex-wrap">
                <Button
                    className="w-1/2"
                    onPress={onDescribe}
                    isLoading={isLoading}
                >
                    Describe Image
                </Button>
                <Button
                    className="w-1/2"
                    onPress={onSave}
                    isLoading={isLoading}
                >
                    Save
                </Button>
            </div>
            <PromptsModal
                isOpen={isPromptModalOpen}
                onOpenChange={setIsPromptModalOpen}
                promptParts={promptItems}
                setPromptParts={setPromptItems}
            />
        </div>
    );
}
