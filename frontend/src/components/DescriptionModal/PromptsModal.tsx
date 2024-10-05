import { Button, Input, Modal, ModalBody, ModalContent, ModalFooter, ModalHeader } from '@nextui-org/react';
import { useEffect, useState } from 'react';
import { IoMdClose } from 'react-icons/io';

type PromptsModalProps = {
    isOpen: boolean;
    onOpenChange: (isOpen: boolean) => void;
    promptParts: string[];
    setPromptParts: (promptParts: string[]) => void;
};

export default function PromptsModal({isOpen, promptParts, onOpenChange, setPromptParts}: PromptsModalProps) {
    const [parts, setParts] = useState<string[]>(promptParts);

    useEffect(() => {
        setParts(promptParts);
    }, [promptParts]);

    return (
        <Modal
            isOpen={isOpen}
            onOpenChange={onOpenChange}
        >
            <ModalContent>
                <ModalHeader>
                    Edit Or Add Prompts
                </ModalHeader>
                <ModalBody>
                    <div className='w-full flex flex-col gap-2'>
                        {
                            parts.map((part, index) => (
                                <div key={index} className='w-full inline-flex'>
                                    <Input
                                        value={part}
                                        onChange={(e) => {
                                            const newParts = [...parts];
                                            newParts[index] = e.target.value;
                                            setParts(newParts);
                                        }}
                                    />
                                    <Button
                                        isIconOnly={true}
                                        onPress={() => {
                                            setParts(parts.filter((_, i) => i !== index));
                                        }}
                                    >
                                        <IoMdClose />
                                    </Button>
                                </div>
                            ))
                        }
                        <Button
                            className='w-full'
                            onPress={() => {
                                setParts([...parts, '']);
                            }}
                        >
                            Add Prompt
                        </Button>
                    </div>
                </ModalBody>
                <ModalFooter>
                    <Button
                        className='w-full'
                        color='primary'
                        onClick={() => {
                            setPromptParts(parts);
                            onOpenChange(false);
                        }}
                    >
                        Save
                    </Button>
                </ModalFooter>
            </ModalContent>
        </Modal>
    );
}
