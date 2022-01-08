export const general = {
    id: '',
    url: '',
    cover: '',
    title: '',
    description: '',
};

export const getAnswer = () => {
    return {
        text: '',
        value: '',
    };
};

export const getQuestion = () => {
    return {
        text: '',
        image: '',
        answers: [
            getAnswer(),
            getAnswer(),
            getAnswer(),
            getAnswer(),
        ],
    };
};

export const getResult = () => {
    return {
        image: '',
        header: '',
        text: '',
        shareUrl: '',
    };
};

export const questions = [
    getQuestion(),
];

export const results = [
    getResult(),
];