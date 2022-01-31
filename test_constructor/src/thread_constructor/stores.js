import {writable} from 'svelte/store';

export function thread() {
    const card = {
        title: '',
        data: {},
    };
    const _thread = {
        general: {
            title: '',
            cover: '',
        },
        cards: [card],
    };
    const {subscribe, set, update} = writable(_thread);

    return {
        subscribe,
        removeCard: (index) => update((t) => {
            t.cards.splice(index, 1);
            return t;
        }),
        addCard: () => update((t) => {
            t.cards.add(card);
            return t;
        }),
    };
}