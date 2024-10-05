import {
    Modal,
    ModalBody,
    ModalContent,
    ModalFooter,
    ModalHeader,
    Image,
    Textarea,
} from '@nextui-org/react';
import { GiTalk } from 'react-icons/gi';
import { FaSave } from 'react-icons/fa';
import useDescriptionModalState from 'app/hooks/useDescriptionModalState.ts';
import useGetDescription from './hooks/useGetDescription.ts';
import useDescriptionData from './hooks/useDescriptionData.ts';
import DescriptionPrompt from './DescriptionPrompt.tsx';
import DescriptionSelect from './DescriptionSelect.tsx';
import { useEffect, useState } from 'react';

export default function DescriptionModal() {
    const { isOpen, onOpenChange } = useDescriptionModalState();
    useGetDescription({ isOpen });
    const descriptionData = useDescriptionData();
    const [isSaved, setIsSaved] = useState<boolean>(false);
    const [isDescribed, setIsDescribed] = useState<boolean>(false);
    const [isLoading, setIsLoading] = useState<boolean>(false);

    const onSavedCallback = () => {
        setIsSaved(true);
        setIsLoading(false);
    };
    const onLoadingCallback = () => {
        setIsLoading(true);
    };

    const onDescribedCallback = () => {
        setIsDescribed(true);
        setIsLoading(false);
    };

    useEffect(() => {
        if (descriptionData?.every(({ value }) => value)) {
            setIsDescribed(true);
        } else {
            setIsSaved(false);
        }
    }, [descriptionData]);

    return (
        <>
            <Modal
                size="5xl"
                isOpen={isOpen}
                isDismissable={!isLoading}
                hideCloseButton={isLoading}
                onOpenChange={onOpenChange}
                classNames={{
                    wrapper: 'overflow-hidden',
                }}
            >
                <ModalContent className="h-full">
                    <ModalHeader className="text-2xl">
                        Description
                        {isDescribed && <GiTalk color="green" />}
                        {isSaved && <FaSave color="green" />}
                    </ModalHeader>
                    <ModalBody className="overflow-y-auto">
                        <div className="flex flex-col gap-5 p-x-10">
                            <div className="flex flex-row gap-5 flex-wrap">
                                <div className="flex-shrink-0 max-w-[200px] h-200 w-200 max-h-[200px]">
                                    <Image
                                        // @ts-expect-error: url is not defined
                                        src={window.url}
                                        className="w-auto h-auto max-w-full max-h-[200px]"
                                    />
                                </div>
                                <DescriptionPrompt
                                    onDescribedCallback={onDescribedCallback}
                                    onSavedCallback={onSavedCallback}
                                    onLoadingCallback={onLoadingCallback}
                                />
                            </div>
                            <div className="flex flex-col gap-2">
                                {
                                    descriptionData.map(({ name, value, onChange, ...d }, index) => (
                                        !['places', 'hashtags'].includes(name) ? (
                                            <Textarea
                                                value={value as string}
                                                onChange={onChange as ((e: any) => unknown)}
                                                isDisabled={isLoading}
                                                minRows={1}
                                                {...d}
                                                key={index}
                                            />
                                        ) : (
                                            <DescriptionSelect
                                                isDisabled={isLoading}
                                                label={d.label}
                                                value={value as Array<string>}
                                                onChange={onChange as (items: Array<string>) => unknown}
                                                key={index}
                                            />
                                        )
                                    ))
                                }
                            </div>
                        </div>
                    </ModalBody>
                    <ModalFooter />
                </ModalContent>
            </Modal>
        </>
    );
}
