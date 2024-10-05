interface BaseModalState {
    isOpen: boolean;
}

export interface AuthorizationModalState extends BaseModalState {}

export interface ControlPanelState extends BaseModalState {}

export interface DescriptionModalState extends BaseModalState {}

export interface DuplicatesModalState extends BaseModalState {}

export interface LookAlikesModalState extends BaseModalState {}

export interface SpinnerModalState extends BaseModalState {}

export interface DialogModalState extends BaseModalState {
    title?: string;
    content?: string;
    confirmed?: boolean;
}
