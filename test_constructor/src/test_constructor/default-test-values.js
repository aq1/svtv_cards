export const getGeneral = () => {
    return {
        id: '',
        url: '',
        cover: '',
        title: '',
        description: '',
        slug: '',
    };
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

export const getTest = () => {
    return {
        general: getGeneral(),
        questions: [getQuestion()],
        results: [getResult()],
    };
};

export const API_URL = '/webhook/test-constructor';
