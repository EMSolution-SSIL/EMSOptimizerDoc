import Link from '@docusaurus/Link';
import Translate, { translate } from '@docusaurus/Translate';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import Heading from '@theme/Heading';
import Layout from '@theme/Layout';
import clsx from 'clsx';
import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle">
          <Translate id="homepage.tagline">
            電気機器に特化した数理最適化ツール
          </Translate>
        </p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/docs/intro">
            <Translate id="homepage.getStarted">はじめる</Translate>
          </Link>
        </div>
      </div>
    </header>
  );
}

function TranslationNotice() {
  const {i18n} = useDocusaurusContext();

  if (i18n.currentLocale !== 'en') {
    return null;
  }

  return (
    <div className={clsx('container', styles.translationNotice)}>
      <p>
        <Translate id="homepage.translationNotice.assistance">
          この英語版ドキュメントはAIを利用して翻訳しています。
        </Translate>{' '}
        <Translate id="homepage.translationNotice.report">
          誤訳や不明瞭な表現を見つけた場合は、
        </Translate>{' '}
        <Link href="https://github.com/EMSolution-SSIL/EMSOptimizerDoc">GitHub Issues</Link>
        <Translate id="homepage.translationNotice.reportSuffix">
          からお知らせください。
        </Translate>
      </p>
    </div>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`${siteConfig.title}`}
      description={translate({
        id: 'homepage.metaDescription',
        message: 'EMSOptimizerの公式ドキュメントサイト',
      })}>
      <HomepageHeader />
      <main>
        <HomepageFeatures />
        <TranslationNotice />
      </main>
    </Layout>
  );
}
