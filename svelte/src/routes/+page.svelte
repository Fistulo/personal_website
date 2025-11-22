<script lang="ts">
  import { Accordion } from "bits-ui";
  import CaretDown from "phosphor-svelte/lib/CaretDown";

  type FaqItem = {
    value: string;
    question: string;
    answer: string;
    isLoading?: boolean;
  };

  type Language = 'en' | 'de';
  let currentLang: Language = 'de';

  let openItems: string[] = [];

  // Translations
  const translations = {
    en: {
      title: "Lennart Lais",
      subtitle: "mini text about me",
      placeholder: "Ask your own question...",
      askButton: "Ask",
      loading: "Loading answer...",
      error: "Sorry, I couldn't get an answer. Please try again.",
      langButton: "DE"
    },
    de: {
      title: "Lennart Lais",
      subtitle: "Ein kleiner Text über mich",
      placeholder: "Stelle deine eigene Frage...",
      askButton: "Fragen",
      loading: "Antwort wird geladen...",
      error: "Entschuldigung, ich konnte keine Antwort erhalten. Bitte versuche es erneut.",
      langButton: "EN"
    }
  };

  $: t = (key: keyof typeof translations.en) => translations[currentLang][key];

  function toggleLanguage() {
    currentLang = currentLang === 'en' ? 'de' : 'en';
  }

  // FAQ items with translations
  let faq_items_data = {
    en: [
      {
        value: "faq_1",
        question: "Question 1?",
        answer: "Answer to question 1.",
      },
      {
        value: "faq_2",
        question: "Question 2?",
        answer: "Answer to question 2.",
      }
    ],
    de: [
      {
        value: "faq_1",
        question: "Frage 1?",
        answer: "Antwort auf Frage 1.",
      },
      {
        value: "faq_2",
        question: "Frage 2?",
        answer: "Antwort auf Frage 2.",
      }
    ]
  };

  let user_questions: FaqItem[] = [];
  let newQuestion = "";
  let isSubmitting = false;

  // Reactive combined items
  $: faq_items = [...faq_items_data[currentLang], ...user_questions];

  async function addQuestion() {
    if (newQuestion.trim() && !isSubmitting) {
      isSubmitting = true;
      const questionValue = `faq_${Date.now()}`;

      // Add item with loading state
      const newItem: FaqItem = {
        value: questionValue,
        question: newQuestion,
        answer: t('loading'),
        isLoading: true
      };
      user_questions = [...user_questions, newItem];

      openItems = [...openItems, questionValue];

      const currentQuestion = newQuestion;
      newQuestion = ""; // Clear input immediately

      try {
        // Call backend API with language context
        const response = await fetch('/api/ask', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ 
            question: currentQuestion,
            language: currentLang === 'en' ? 'English' : 'Deutsch'
          })
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // Update the answer
        user_questions = user_questions.map(item => 
          item.value === questionValue 
            ? { ...item, answer: data.answer, isLoading: false }
            : item
        );
      } catch (error) {
        console.error('Error fetching answer:', error);

        // Update with error message
        user_questions = user_questions.map(item => 
          item.value === questionValue 
            ? { ...item, answer: t('error'), isLoading: false }
            : item
        );
      } finally {
        isSubmitting = false;
      }
    }
  }

  function handleKeydown(event: KeyboardEvent) {
    if (event.key === "Enter") {
      addQuestion();
    }
  }
</script>

<div class="flex flex-col items-center w-full px-4 mt-12 md:mt-20">
  <!-- Language Toggle Button -->
  <button
    on:click={toggleLanguage}
    class="fixed top-4 right-4 z-50 px-4 py-2 bg-white border-2 border-gray-300 rounded-lg font-medium hover:bg-gray-50 transition-colors shadow-sm"
    aria-label="Toggle language"
  >
    {t('langButton')}
  </button>

  <!-- Hero Section -->
  <div class="grid grid-cols-1 md:grid-cols-2 gap-8 w-full max-w-4xl mb-12 items-center">
    <div class="order-2 md:order-1">
      <h1 class="text-4xl md:text-5xl font-bold mb-4">{t('title')}</h1>
      <p class="text-lg text-gray-600">{t('subtitle')}</p>
    </div>
    <img 
      src="piohela_bild.jpg" 
      alt="Portrait Lennart Lais" 
      class="order-1 md:order-2 w-full max-w-sm mx-auto rounded-lg shadow-lg object-cover aspect-square"
    />
  </div>

  <!-- FAQ Section -->
  <Accordion.Root class="w-full max-w-4xl" type="multiple" bind:value={openItems}>
    {#each faq_items as item (item.value)}
      <Accordion.Item
        value={item.value}
        class="border-dark-10 group border-b px-1.5"
      >
        <Accordion.Header>
          <Accordion.Trigger
            class="flex w-full flex-1 select-none items-center justify-between py-5 text-[15px] font-medium transition-all [&[data-state=open]>span>svg]:rotate-180"
          >
            <span class="w-full text-left">
              {item.question}
            </span>
            <span
              class="hover:bg-dark-10 inline-flex size-8 items-center justify-center rounded-[7px] bg-transparent"
            >
              <CaretDown class="size-[18px] transition-transform duration-200" />
            </span>
          </Accordion.Trigger>
        </Accordion.Header>
        <Accordion.Content
          class="data-[state=closed]:animate-accordion-up data-[state=open]:animate-accordion-down overflow-hidden text-sm tracking-[-0.01em]"
        >
          <div class="pb-[25px]">
            {item.answer}
          </div>
        </Accordion.Content>
      </Accordion.Item>
    {/each}

    <!-- Add Question Input -->
    <div class="border-dark-10 border-b px-1.5">
      <div class="flex w-full items-center justify-between py-5 gap-3">
        <input
          type="text"
          bind:value={newQuestion}
          on:keydown={handleKeydown}
          placeholder={t('placeholder')}
          disabled={isSubmitting}
          class="flex-1 text-[15px] font-medium bg-transparent outline-none placeholder:text-gray-400 disabled:opacity-50"
        />
        <button
          on:click={addQuestion}
          disabled={!newQuestion.trim() || isSubmitting}
          class="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
        >
          {t('askButton')}
        </button>
      </div>
    </div>
  </Accordion.Root>
</div>
