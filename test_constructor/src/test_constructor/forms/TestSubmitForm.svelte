<script>
    import Button from '../../components/Button.svelte';
    export let test;

    const submitTest = () => {

    };
</script>

<div class="test-submit">
  <div class="test-submit__header">
    Тест: <span class="test-submit__header-test">{test.general.title}</span>
  </div>

  <div class="test-submit__description">
    {test.general.description}
  </div>

  <div class="test-submit__cover">
    <img src="{test.general.cover}" alt="обложка теста">
  </div>

  <div class="test-submit__questions">
    Вопросов: {test.questions.length}
  </div>
  <div class="test-submit__results">
    Результатов: {test.results.length}
  </div>
  <div class="test-submit__button">
    <Button text="Сохранить" callback={submitTest} className="success"/>
  </div>
</div>

<style>
    .test-submit {
        display: flex;
        flex-direction: column;
        gap: 10px;
        font-size: 1.1em;
    }

    .test-submit__header-test {
        font-weight: bold;
    }
</style>
