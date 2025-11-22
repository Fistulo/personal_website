<script lang="ts">
  import { Accordion } from "bits-ui";
  import CaretDown from "phosphor-svelte/lib/CaretDown";

  type FaqItem = {
    value: string;
    question: string;
    answer: string;
    isLoading: boolean;
  };

  type Language = 'en' | 'de';
  let currentLang: Language = 'de';

  let openItems: string[] = [];

  // Translations
  const translations = {
    en: {
      title: "Lennart Lais",
      subtitle: "CS student | Outdoor enjoyer",
      subtext: "Welcome to my little website! Ask me some questions and learn more about me.",
      placeholder: "Ask your own question...",
      askButton: "Ask",
      loading: "Loading answer...",
      error: "Sorry, I couldn't get an answer. Please try again.",
      langButton: "DE"
    },
    de: {
      title: "Lennart Lais",
      subtitle: "Informatik Student | Outdoor Geniesser",
      subtext: "Willkommen auf meiner kleinen Website! Stelle mir ein paar Fragen und lerne mich kennen",
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
        question: "What are your hobbies?",
        answer: "I was active in the scouts for a long time and am still involved in a few projects. I enjoy hiking and camping in nature. And finally, I'm deep into the world of coffee and even filter the water for my coffee.",
        isLoading: false
      },
      {
        value: "faq_2",
        question: "I heard you're looking for an internship?",
        answer: "Exactly! I'm looking for an internship in software development starting March 2025 for 6 months. If you're interested, just get in touch!",
        isLoading: false
      }
    ],
    de: [
      {
        value: "faq_1",
        question: "Was sind deine Hobbies?",
        answer: "Ich war lange Zeit in der Pfadi aktiv, und bin immer noch in ein paar Projekten involviert. Ich bin gerne in der Natur am Wandern und auch Campen. Und schliesslich bin ich tief in der Kaffee-Welt und filtere sogar das Wasser für meinen Kaffee.",
        isLoading: false
      },
      {
        value: "faq_2",
        question: "Ich habe gehört du sucht ein Praktikum?",
        answer: "Ganz genau! Ich suche ein Praktikum im Bereich Softwareentwicklung ab März 2025 für 6 Monate. Bei Interesse einfach melden!",
        isLoading: false
      }
    ]
  };

  let user_questions: FaqItem[] = [];
  let newQuestion = "";
  let isSubmitting = false;

  // Reactive combined items
  $: faq_items = [...faq_items_data[currentLang], ...user_questions];
  $: nextIndex = faq_items.length;
  $: buttonBgColor = `hsl(${(120 + 12 * nextIndex) % 360}, 60%, 75%)`;
  $: buttonHoverColor = `hsl(${(120 + 12 * nextIndex) % 360}, 60%, 65%)`;

  function handleButtonMouseEnter(e: MouseEvent) {
    if (!newQuestion.trim() || isSubmitting) return;
    (e.currentTarget as HTMLElement).style.backgroundColor = buttonHoverColor;
  }

  function handleButtonMouseLeave(e: MouseEvent) {
    if (!newQuestion.trim() || isSubmitting) return;
    (e.currentTarget as HTMLElement).style.backgroundColor = buttonBgColor;
  }

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
      <p class="text-lg text-gray-600 italic">{t('subtitle')}</p>
      <p class="text-lg text-gray-600">{t('subtext')}</p>
    </div>
    <img 
      src="piohela_bild.jpg" 
      alt="Portrait Lennart Lais" 
      class="order-1 md:order-2 w-full max-w-sm mx-auto mx-auto md:mx-0 md:ml-auto rounded-lg shadow-lg object-cover aspect-square"
    />
  </div>

  <!-- FAQ Section -->
  <Accordion.Root class="w-full max-w-4xl" type="multiple" bind:value={openItems}>
    {#each faq_items as item, index (item.value)}
      {@const bgColor = `hsl(${(120 + 12 * index) % 360}, 60%, 75%)`}
      {@const lighterBgColor = `hsl(${(120 + 12 * index) % 360}, 60%, 85%)`}
      <Accordion.Item
        value={item.value}
        class="group overflow-hidden mb-4 rounded-xl shadow-lg"
        style="background-color: {bgColor}"
      >
        <Accordion.Header>
          <Accordion.Trigger
            class="flex w-full flex-1 select-none items-center justify-between py-5 px-1.5 text-base md:text-lg lg:text-lg font-medium transition-all [&[data-state=open]>span>svg]:rotate-180"
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
          class="data-[state=closed]:animate-accordion-up data-[state=open]:animate-accordion-down overflow-hidden text-sm md:text-base lg:text-base tracking-[-0.01em]"
        >
          <div 
            class="px-1.5 py-5 {item.isLoading ? 'loading-wave' : ''}"
            style="background-color: {lighterBgColor}"
          >
            {item.answer}
          </div>
        </Accordion.Content>
      </Accordion.Item>
    {/each}

    <!-- Add Question Input -->
    <div class="border-2 border-gray-300 rounded-xl shadow-lg mb-4 transition-colors focus-within:border-gray-500">
      <div class="flex w-full items-center justify-between py-[18px] px-1.5">
        <input
          type="text"
          bind:value={newQuestion}
          on:keydown={handleKeydown}
          placeholder={t('placeholder')}
          disabled={isSubmitting}
          maxlength="150"
          class="flex-1 text-base md:text-lg lg:text-lg font-medium bg-transparent outline-none placeholder:text-gray-400 disabled:opacity-50 focus-overrite"
          style="outline: none !important; box-shadow: none !important; border: none !important;"
        />
        <button
          on:click={addQuestion}
          on:mouseenter={handleButtonMouseEnter}
          on:mouseleave={handleButtonMouseLeave}
          disabled={!newQuestion.trim() || isSubmitting}
          class="px-4 py-2 text-white rounded-lg text-base md:text-lg lg:text-lg font-medium disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
          style="background-color: {!newQuestion.trim() || isSubmitting ? '' : buttonBgColor}"
        >
          {t('askButton')}
        </button>
      </div>
    </div>
  </Accordion.Root>
</div>