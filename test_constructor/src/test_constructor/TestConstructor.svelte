<script>
    import {onMount} from 'svelte';
    import {Splide, SplideSlide} from '@splidejs/svelte-splide';
    import TestSelectForm from './forms/TestSelectForm.svelte';
    import TestGeneralForm from './forms/TestGeneralForm.svelte';
    import TestQuestionsForm from './forms/TestQuestionsForm.svelte';
    import TestResultsForm from './forms/TestResultsForm.svelte';
    import TestSubmitForm from './forms/TestSubmitForm.svelte';
    import SplideControls from '../components/SplideControls.svelte';
    import '@splidejs/splide/dist/css/splide.min.css';

    import {getTest, API_URL} from './default-test-values';

    let splide;
    let tests;
    let test;

    const options = {
        perPage: 1,
        gap: '10px',
        perMove: 1,
        arrows: false,
        pagination: false,
        keyboard: false,
        drag: false,
        wheel: false,
        width: '100%',
        waitForTransition: false,
    };

    const slides = [
        'Выбрать тест',
        'Основное',
        'Вопросы',
        'Результаты',
        'Сохранить',
    ];

    const getTests = () => {
        fetch(`${API_URL}/tests/`).then((response) => {
            response.json().then((json) => {
                tests = [];
                for (let t of json.tests) {
                    tests = [...tests, JSON.parse(t)];
                }
            });
        });
        test = getTest();
    };
    onMount(getTests);
</script>
<div class="slider">
  {#if tests}
    <SplideControls {slides} {splide}/>
    <Splide {options} bind:this={ splide }>
      <SplideSlide>
        <TestSelectForm {tests} bind:test/>
      </SplideSlide>
      <SplideSlide>
        <TestGeneralForm bind:data={test.general}/>
      </SplideSlide>
      <SplideSlide>
        <TestQuestionsForm bind:questions={test.questions}/>
      </SplideSlide>
      <SplideSlide>
        <TestResultsForm bind:results={test.results}/>
      </SplideSlide>
      <SplideSlide>
        <TestSubmitForm bind:test/>
      </SplideSlide>
    </Splide>
  {:else}
    Loading...
  {/if}
  <pre>
    {JSON.stringify(test, null, 2)}
  </pre>

</div>


<style>
    .slider {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    pre {
        overflow: hidden;
    }
</style>