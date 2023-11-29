export const GUESS_CATEGORIES = ['Gender', 'Race', 'Allegiance', 'Infected', 'Profession', 'Rarity', 'Cost']

export function randomInteger(min: number, max: number) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

export const ICON_DIR = 'https://raw.githubusercontent.com/Three6ty1/ak-wordle-icons/main/avatars/'

export enum OPERATOR_RESULTS {
    name = 0,
    charId = 1,
    rarity = 2,
}