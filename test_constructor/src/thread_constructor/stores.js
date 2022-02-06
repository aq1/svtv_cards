import {writable} from 'svelte/store';


function createThread() {
    const defaultThread = {
        general: {
            id: '',
            title: '',
            cover: '',
            url: '',
            slug: '',
        },
        cards: [
            {
                title: '',
                isActive: false,
                data: {},
            }
        ],
    };

    const {subscribe, set, update} = writable(defaultThread);
    return {
        subscribe,
        set,
        reset: () => {
            set(defaultThread);
        },
        addCard: () => update((thread) => {
            const cards = [...thread.cards, {
                title: '',
                isActive: false,
                data: {},
            }];
            return {
                ...thread,
                cards,
            };
        }),
        removeCard: (index) => update((thread) => {
            const cards = thread.cards;
            cards.splice(index, 1);
            return {
                ...thread,
                cards,
            };
        }),
        setActiveCard: (index) => {
            update((thread) => {
                thread.cards.forEach((card, cardIndex) => {
                    card.isActive = index === cardIndex;
                });
                return thread;
            });
        },
        moveCard: (index, direction) => {
            update((thread) => {
                if (index + direction < 0 || index + direction >= thread.cards.length) {
                    return thread;
                }

                thread.cards.forEach((card) => {card.isActive = false});

                thread.cards.splice(
                    index + direction,
                    0,
                    thread.cards.splice(index, 1)[0],
                );
                return thread;

            });
        },
    };
}

export const thread = createThread();
